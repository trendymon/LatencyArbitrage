from QLearning.pipe import *

# Create named pipes for all terminals
terminal_sender = Pipe("send")
terminal_sender2 = Pipe("send")
terminal_receiver = Pipe("gerchik")
terminal_receiver2 = Pipe("tickmill")

# set difference between broker's prices
DELTA_TICKS = 0.00020
# set commands to clients
OP_BUY = 0
OP_SELL = 1

if terminal_sender.is_connect():
    if terminal_sender2.is_connect():
        while True:
            data1 = terminal_sender.read_as_string(1024).split(',')
            data2 = terminal_sender2.read_as_string(1024).split(',')

            for i in range(2, 6):
                data1[i] = float(data1[i])
            for i in range(2, 6):
                data2[i] = float(data2[i])

            bid1, ask1, time1 = data1[2], data1[3], data1[4]
            bid2, ask2, time2 = data2[2], data2[3], data2[4]

            if data1[1] == data2[1]:
                if time1 > time2:
                    if bid1 - ask2 > DELTA_TICKS:
                        terminal_receiver.write([OP_SELL, bid1 - (bid1 - ask2)])
                        print(data1[0], 'SELL', data1[1], 'TARGET', bid1 - (bid1 - ask2))
                    if bid2 - ask1 > DELTA_TICKS:
                        terminal_receiver.write([OP_BUY, ask1 + (bid2 - ask1)])
                        print(data1[0], 'BUY', data1[1], 'TARGET', ask1 + (bid2 - ask1))

                if time2 > time1:
                    if bid2 - ask1 > DELTA_TICKS:
                        terminal_receiver2.write([OP_SELL, bid2 - (bid2 - ask1)])
                        print(data2[0], 'SELL', data2[1], 'TARGET', bid2 - (bid2 - ask1))
                    if bid1 - ask2 > DELTA_TICKS:
                        terminal_receiver2.write([OP_BUY, ask2 + (bid1 - ask2)])
                        print(data2[0], 'BUY', data2[1], 'TARGET', ask2 + (bid1 - ask2))

            terminal_receiver.write('(wait signal)')
            terminal_receiver2.write('(wait signal)')
