from nsepy import get_history
from datetime import datetime
import matplotlib.pyplot as plt

from AbstractModule import AbstractCommand


class Command(AbstractCommand):

    def get_command_code(self):
        return "nsehist"

    def get_command_desc(self):
        return "Provides history of a stock from NSE market"

    def add_options(self, parser):
        # Add applicable arguments and parse
        parser.add_argument("-b", "--beginDate", help="Begin Date", required=True)
        parser.add_argument("-e", "--endDate", help="End Date", required=True)
        parser.add_argument("-p", "--plotType", help="Plot Type")
        parser.add_argument("-s", "--symbol", help="Stock/Instrument Code", required=True)
        parser.add_argument("-i", "--index", help="Index", action='store_true')
        parser.add_argument("-f", "--futures", help="Futures", action='store_true')
        parser.add_argument("-g", "--no-graph", help="Graph Not Required", action='store_false')
        return

    # Entry to command execution
    def main(self, args):
        if args.plotType is not None:
            plt.style.use(str(args.plotType))
        else:
            plt.style.use('fivethirtyeight')

        from_date = datetime.strptime(args.beginDate, '%Y-%m-%d')
        to_date = datetime.strptime(args.endDate, '%Y-%m-%d')
        data = get_history(symbol=args.symbol, start=from_date, end=to_date, index=args.index, futures=args.futures)
        print(data)
        if args.no_graph is True:
            data['Close'].plot()
            plt.show()
