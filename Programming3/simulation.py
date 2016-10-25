'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import network
import link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0  # 0 means unlimited
simulation_time = 1  # give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = []  # keeps track of objects, so we can kill their threads

    aTable = {0:0, 1:1}
    bTable = {0:0}
    cTable = {0:0}
    dTable = {0:0, 1:0}
    # create network nodes
    host1 = network.Host(1)
    object_L.append(host1)
    host2 = network.Host(2)
    object_L.append(host2)
    host3 = network.Host(3)
    object_L.append(host3)
    router_a = network.Router(name='A', intf_count_in=2, intf_count_out=2, max_queue_size=router_queue_size, inLUT=aTable)
    object_L.append(router_a)
    router_b = network.Router(name='B', intf_count_in=1, intf_count_out=1, max_queue_size=router_queue_size, inLUT=bTable)
    object_L.append(router_b)
    router_c = network.Router(name='C', intf_count_in=1, intf_count_out=1, max_queue_size=router_queue_size, inLUT=cTable)
    object_L.append(router_c)
    router_d = network.Router(name='D', intf_count_in=2, intf_count_out=1, max_queue_size=router_queue_size, inLUT=dTable)
    object_L.append(router_d)

    # create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)

    # add all the links
    link_layer.add_link(link.Link(host1, 0, router_a, 0, 50))       #H1:0 - RA:0
    link_layer.add_link(link.Link(host2, 0, router_a, 1, 50))       #H2:0 - RA:1
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))    #RA:0 - RB:0
    link_layer.add_link(link.Link(router_a, 1, router_c, 0, 50))    #RA:1 - RC:0
    link_layer.add_link(link.Link(router_b, 0, router_d, 0, 50))    #RB:0 - RD:0
    link_layer.add_link(link.Link(router_c, 0, router_d, 1, 50))    #RC:0 - RD:1
    link_layer.add_link(link.Link(router_d, 0, host3, 0, 50))       #RD:0 - H3:0

    # start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=host1.__str__(), target=host1.run))
    thread_L.append(threading.Thread(name=host2.__str__(), target=host2.run))
    thread_L.append(threading.Thread(name=host3.__str__(), target=host3.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))

    thread_L.append(threading.Thread(name="Network", target=link_layer.run))

    for t in thread_L:
        t.start()

    message = "12345678901234567890123456789012345678901234567890123456789012345678901234567890"
    host1.udt_send(3, message)
    host2.udt_send(3, message)
    # create some send events
    for i in range(3):
        host1.udt_send(2, 'Sample data %d' % i)

    for i in range(3):
        host2.udt_send(2, 'Sample data %d' % i)

    # give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)

    # join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")



    # writes to host periodically
