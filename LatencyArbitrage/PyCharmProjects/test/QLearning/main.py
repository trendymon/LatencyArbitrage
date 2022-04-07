from QLearning.pipe import Pipe
from time import gmtime, strftime

# Create named pipes for all terminals
terminal_sender = Pipe("send")
terminal_sender2 = Pipe("send")
terminal_receiver = Pipe("gerchik")
terminal_receiver2 = Pipe("tickmill")

# set difference between broker's prices
DELTA_TICKS = 0.0003
# set commands to clients
OP_BUY = 0
OP_SELL = 1

print(DELTA_TICKS)
if terminal_sender.is_connect():
    if terminal_sender2.is_connect():
        while True:
            data1 = terminal_sender.read_as_string(1024).split(',')
            data2 = terminal_sender2.read_as_string(1024).split(',')

            for i in range(2, 5):
                data1[i] = float(data1[i])
            for i in range(2, 5):
                data2[i] = float(data2[i])

            mid1, buy_orders1, sell_orders1 = data1[2], data1[3], data1[4]
            mid2, buy_orders2, sell_orders2 = data2[2], data2[3], data2[4]

            if data1[1] == data2[1]:
                if mid1 - mid2 > DELTA_TICKS:
                    terminal_receiver2.write([OP_BUY])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'BUY', data2[1])
                    terminal_receiver.write([OP_SELL])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'SELL', data1[1])

                elif mid2 - mid1 > DELTA_TICKS:
                    terminal_receiver2.write([OP_SELL])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data2[0], 'SELL', data2[1])
                    terminal_receiver.write([OP_BUY])
                    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), data1[0], 'BUY', data1[1])

                elif DELTA_TICKS / 3 > mid1 - mid2 > 0:
                    terminal_receiver.write(2)
                    terminal_receiver2.write(2)

                elif DELTA_TICKS / 3 > mid2 - mid1 > 0:
                    terminal_receiver2.write(2)
                    terminal_receiver.write(2)

                else:
                    terminal_receiver.write('-')
                    terminal_receiver2.write('-')
