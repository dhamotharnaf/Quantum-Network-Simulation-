
from qunetsim.components.host import Host
from qunetsim.components.network import Network
from qunetsim.objects import Qubit
from qunetsim.objects import Logger
Logger.DISABLED = True


def protocol_1(host, receiver):
    # Here we write the protocol code for a host.
    for i in range(5):
        q = Qubit(host)
        # Apply Hadamard gate to the qubit
        q.H()
        print('Sending qubit %d.' % (i+1))
        # Send qubit and wait for an acknowledgement
        host.send_qubit(receiver, q, await_ack=True)
        print('Qubit %d was received by %s.' % (i+1, receiver))


def protocol_2(host, sender):
    # Here we write the protocol code for another host.
    for _ in range(5):
        # Wait for a qubit from Alice for 10 seconds.
        q = host.get_data_qubit(sender, wait=10)
        # Measure the qubit and print the result.
        print('%s received a qubit in the %d state.' % (host.host_id, q.measure()))


def main():
   network = Network.get_instance()
   nodes = ['jhon', 'murphy', 'dhamu', 'Sidharth']
   network.start(nodes)

   host_A = Host('jhon')
   host_A.add_connection('murphy')
   host_A.add_connection('dhamu')
   host_A.add_connection('Sidharth')
   host_A.start()
   host_B = Host('murphy')
   host_B.add_connection('jhon')
   host_B.add_connection('dhamu')
   host_B.add_connection('Sidharth')
   host_B.start()
   host_C = Host('dhamu')
   host_C.add_connection('jhon')
   host_C.add_connection('murphy')
   host_C.add_connection('Sidharth')
   host_C.start()
   host_D = Host('Sidharth')
   host_D.add_connection('jhon')
   host_D.add_connection('murphy')
   host_D.add_connection('dhamu')
   host_D.start()

   network.add_host(host_A)
   network.add_host(host_B)
   network.add_host(host_C)
   network.add_host(host_D)

   host_A.run_protocol(protocol_1, (host_D.host_id,))
   host_D.run_protocol(protocol_2, (host_A.host_id,))

if __name__ == '__main__':
   main()

 
