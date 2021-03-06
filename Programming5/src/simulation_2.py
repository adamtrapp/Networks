'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import network_2 as network
import link_2 as link
import threading
from time import sleep
import sys

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 10 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads

    #create network hosts
    client1 = network.Host(1)
    object_L.append(client1)
    client2 = network.Host(2)
    object_L.append(client2)
    server = network.Host(3)
    object_L.append(server)

    #create routers and routing tables for connected clients (subnets)
    router_a = network.Router(name='A',
                              intf_cost_L=[1, 1, 1, 1],
                              intf_capacity_L=[500, 500, 500, 500],
                              rt_tbl_D={
                                  0: {3: ('0', 2)},
                                  1: {3: ('1', 3)}
                              },
                              fwd_tbl_D={},
                              max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b = network.Router(name='B',
                              intf_cost_L=[1, 1],
                              intf_capacity_L=[500, 500],
                              rt_tbl_D={},
                              fwd_tbl_D={
                                  '0': ('2', 1)
                              },
                              max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c = network.Router(name='C',
                              intf_cost_L=[1, 1],
                              intf_capacity_L=[500, 500],
                              rt_tbl_D={},
                              fwd_tbl_D={
                                  '1': ('3', 1),
                              },
                              max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d = network.Router(name='D',
                              intf_cost_L=[1, 1, 1],
                              intf_capacity_L=[500, 500, 500],
                              rt_tbl_D={},
                              fwd_tbl_D={
                                  '2': (None, 2),
                                  '3': (None, 2),
                              },
                              max_queue_size=router_queue_size)
    object_L.append(router_d)

    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)

    #add all the links
    link_layer.add_link(link.Link(client1, 0, router_a, 0))
    link_layer.add_link(link.Link(client2, 0, router_a, 1))
    link_layer.add_link(link.Link(router_a, 2, router_b, 0))
    link_layer.add_link(link.Link(router_a, 3, router_c, 0))
    link_layer.add_link(link.Link(router_b, 1, router_d, 0))
    link_layer.add_link(link.Link(router_c, 1, router_d, 1))
    link_layer.add_link(link.Link(router_d, 2, server, 0))

    #start all the objects
    thread_L = []
    for obj in object_L:
        thread_L.append(threading.Thread(name=obj.__str__(), target=obj.run))

    for t in thread_L:
        t.start()

    #create some send events
    for i in range(5):
        priority = i % 2
        print(priority)
        client1.udt_send(3, 'Sample client1 data %d' % i, priority)
        client2.udt_send(3, 'Sample client2 data %d' % i, priority)

    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    #print the final routing tables
    for obj in object_L:
        if str(type(obj)) == "<class 'network.Router'>":
            obj.print_routes()

    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")
