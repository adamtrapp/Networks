'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import queue
import threading
from collections import defaultdict


## wrapper class for a queue of packets
class Interface:
    ## @param maxsize - the maximum size of the queue storing packets
    #  @param cost - of the interface used in routing
    #  @param capacity - the capacity of the link in bps
    def __init__(self, cost=0, maxsize=0, capacity=500):
        self.in_queue = queue.Queue(maxsize)
        self.out_queue = {
            0: queue.Queue(maxsize),
            1: queue.Queue(maxsize)
        }
        self.cost = cost
        self.capacity = capacity  # serialization rate
        self.next_avail_time = 0  # the next time the interface can transmit a packet

    ##get packet from the queue interface
    # @param in_or_out - use 'in' or 'out' interface
    def get(self, in_or_out):
        try:
            if in_or_out == 'in':
                pkt_S = self.in_queue.get(False)
                return pkt_S
            else:
                # Enumerate priorities from highest to lowest
                for priority in sorted(self.out_queue.keys(), reverse=True):
                    # If there are no entries in this priority, skip it
                    if self.out_queue[priority].empty():
                        continue

                    # Get the first packet waiting in this priority queue
                    pkt_S = self.out_queue[priority].get(False)
                    return pkt_S
        except queue.Empty:
            return None

    ##put the packet into the interface queue
    # @param pkt - Packet to be inserted into the queue
    # @param in_or_out - use 'in' or 'out' interface
    # @param block - if True, block until room in queue, if False may throw queue.Full exception
    def put(self, pkt_S, in_or_out, block=False, priority=0):
        # Figure out which queue we're putting into
        if in_or_out == 'out':
            put_queue = self.out_queue[priority]
        else:
            put_queue = self.in_queue

        put_queue.put(pkt_S, block)

    def out_queue_empty(self):
        return all(q.empty() for p, q in self.out_queue.items())

    def out_queue_size(self):
        return sum(q.qsize() for p, q in self.out_queue.items())


## Implements a network layer packet (different from the RDT packet
# from programming assignment 2).
# NOTE: This class will need to be extended to for the packet to include
# the fields necessary for the completion of this assignment.
class NetworkPacket:
    ## packet encoding lengths 
    dst_addr_S_offset = 0
    dst_addr_S_length = 5
    prot_S_offset = dst_addr_S_offset + dst_addr_S_length
    prot_S_length = 1
    priority_S_offset = prot_S_offset + prot_S_length
    priority_S_length = 1
    data_S_offset = priority_S_offset + priority_S_length

    ##@param dst_addr: address of the destination host
    # @param data_S: packet payload
    # @param prot_S: upper layer protocol for the packet (data, or control)
    def __init__(self, dst_addr, prot_S, priority_S, data_S):
        self.dst_addr = dst_addr
        self.prot_S = prot_S
        self.priority_S = priority_S
        self.data_S = data_S

    ## called when printing the object
    def __str__(self):
        return self.to_byte_S()

    ## convert packet to a byte string for transmission over links
    def to_byte_S(self):

        # Add the destination address to the byte string
        byte_S = str(self.dst_addr).zfill(self.dst_addr_S_length)

        # Add the protocol value
        if self.prot_S == 'data':
            byte_S += '1'
        elif self.prot_S == 'control':
            byte_S += '2'
        else:
            raise ('%s: unknown prot_S option: %s' % (self, self.prot_S))

        # Add the priority value
        byte_S += str(self.priority_S).zfill(self.priority_S_length)

        # Add the actual data
        byte_S += self.data_S
        return byte_S

    ## extract a packet object from a byte string
    # @param byte_S: byte string representation of the packet
    @classmethod
    def from_byte_S(self, byte_S):

        # Get the destination address
        dst_addr = int(byte_S[self.dst_addr_S_offset: self.dst_addr_S_offset + self.dst_addr_S_length])

        # Get the protocol option
        prot_S = byte_S[self.prot_S_offset: self.prot_S_offset + self.prot_S_length]
        if prot_S == '1':
            prot_S = 'data'
        elif prot_S == '2':
            prot_S = 'control'
        else:
            raise ('%s: unknown prot_S field: %s' % (self, prot_S))

        # Get the priority
        priority_S = int(byte_S[self.priority_S_offset: self.priority_S_offset + self.priority_S_length])

        # Get the data
        data_S = byte_S[self.data_S_offset:]

        # Construct the packet
        return self(dst_addr, prot_S, priority_S, data_S)


class MPLS_frame:
    label_offset = 0
    label_length = 20
    data_S_offset = label_offset + label_length

    def __init__(self, label, data_S):
        self.label = label
        self.data_S = data_S

    def to_byte_S(self):
        # Format in the label
        byte_S = str(self.label).zfill(self.label_length)

        # Format in the data
        byte_S += self.data_S

        return byte_S

    @classmethod
    def from_byte_S(self, byte_S):
        # Parse out the label
        label = byte_S[self.label_offset: self.label_length]

        # Parse out the data
        data_S = byte_S[self.data_S_offset:]

        return self(label, data_S)

    def __len__(self):
        return len(self.to_byte_S())

    def __str__(self):
        return self.to_byte_S()

## Implements a network host for receiving and transmitting data
class Host:
    ##@param addr: address of this node represented as an integer
    def __init__(self, addr):
        self.addr = addr
        self.intf_L = [Interface()]
        self.stop = False  # for thread termination

    ## called when printing the object
    def __str__(self):
        return 'Host_%s' % (self.addr)

    ## create a packet and enqueue for transmission
    # @param dst_addr: destination address for the packet
    # @param data_S: data being transmitted to the network layer
    # @param priority: packet priority
    def udt_send(self, dst_addr, data_S, priority=0):
        p = NetworkPacket(dst_addr, 'data', priority, data_S)
        print('%s: sending packet "%s"' % (self, p))
        self.intf_L[0].put(p.to_byte_S(), 'out', priority=p.priority_S)  # send packets always enqueued successfully

    ## receive packet from the network layer
    def udt_receive(self):
        pkt_S = self.intf_L[0].get('in')
        if pkt_S is not None:
            pkt = NetworkPacket.from_byte_S(pkt_S)
            print('%s: received packet "%s", priority: %d' % (self, pkt_S, pkt.priority_S))

    ## thread target for the host to keep receiving data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            # receive data arriving to the in interface
            self.udt_receive()
            # terminate
            if (self.stop):
                print(threading.currentThread().getName() + ': Ending')
                return


## Implements a multi-interface router described in class
class Router:
    ##@param name: friendly router name for debugging
    # @param intf_capacity_L: capacities of outgoing interfaces in bps
    # @param max_queue_size: max queue length (passed to Interface)
    def __init__(self, name, intf_cost_L, intf_capacity_L, rt_tbl_D, fwd_tbl_D, max_queue_size):
        self.stop = False  # for thread termination
        self.name = name
        # create a list of interfaces
        # note the number of interfaces is set up by out_intf_cost_L
        assert(len(intf_cost_L) == len(intf_capacity_L))
        self.intf_L = []
        for i in range(len(intf_cost_L)):
            self.intf_L.append(Interface(intf_cost_L[i], max_queue_size, intf_capacity_L[i]))
        # set up the routing table for connected hosts
        self.rt_tbl_D = rt_tbl_D
        self.fwd_tbl_D = fwd_tbl_D

    def __str__(self):
        return 'Router_%s' % (self.name)

    ## look through the content of incoming interfaces and
    # process data and control packets
    def process_queues(self):
        for i in range(len(self.intf_L)):
            pkt_S = None
            # get packet from interface i
            pkt_S = self.intf_L[i].get('in')
            # if packet exists make a forwarding decision
            if pkt_S is not None:
                in_label = None

                # If the packet is an MPLS packet
                if isinstance(pkt_S, MPLS_frame):
                    in_label = pkt_S.label
                    pkt_S = pkt_S.data_S

                # Decode the packet
                pkt = NetworkPacket.from_byte_S(pkt_S)
                if pkt.prot_S == 'data':
                    self.forward_packet(pkt, i, in_label)
                elif pkt.prot_S == 'control':
                    self.update_routes(pkt, i)
                else:
                    raise Exception('%s: Unknown packet type in packet %s' % (self, pkt_S))

    ## forward the packet according to the routing table
    #  @param p Packet to forward
    #  @param in_intf Incoming interface number for packet pkt
    #  @param in_label Incoming label for the packet
    def forward_packet(self, pkt, in_intf, in_label):
        try:
            pkt_S = pkt.to_byte_S()

            # If we should forward using MPLS labels
            if in_label is not None:
                (out_label, out_intf) = self.fwd_tbl_D[in_label]
            else:
                (out_label, out_intf) = self.rt_tbl_D[in_intf][pkt.dst_addr]

            # If we found an out label
            if out_label is not None:
                # Wrap the packet in an MPLS frame
                pkt_S = MPLS_frame(out_label, pkt_S)

            # Output the packet
            self.intf_L[out_intf].put(pkt_S, 'out', block=True, priority=pkt.priority_S)
            print('%s: forwarding packet "%s" from interface %d to %d' % (self, pkt, in_intf, out_intf))
        except queue.Full:
            print('%s: packet "%s" lost on interface %d' % (self, pkt, in_intf))
            pass

    ## forward the packet according to the routing table
    #  @param p Packet containing routing information
    def update_routes(self, p, i):
        # TODO: add logic to update the routing tables and
        # possibly send out routing updates
        print('%s: Received routing update %s from interface %d' % (self, p, i))

    ## send out route update
    # @param i Interface number on which to send out a routing update
    def send_routes(self, i):
        # a sample route update packet
        p = NetworkPacket(0, 'control', 0, 'Sample routing table packet')
        try:
            # TODO: add logic to send out a route update
            print('%s: sending routing update "%s" from interface %d' % (self, p, i))
            self.intf_L[i].put(p.to_byte_S(), 'out', block=True, priority=p.priority_S)
        except queue.Full:
            print('%s: packet "%s" lost on interface %d' % (self, p, i))
            pass

    ## Print routing table
    def print_routes(self):
        print('%s: routing table' % self)
        # TODO: print the routes as a two dimensional table for easy inspection
        # Currently the function just prints the route table as a dictionary
        print(self.rt_tbl_D)

    ## thread target for the host to keep forwarding data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            self.process_queues()
            if self.stop:
                print(threading.currentThread().getName() + ': Ending')
                return
