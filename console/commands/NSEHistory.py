from nsepy import get_history
from nsepy.derivatives import get_expiry_date

import Utils
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
        parser.add_argument("-x", "--expiryDate", help="Expiry Date")
        parser.add_argument("-p", "--plotType", help="Plot Type")
        parser.add_argument("-o", "--optionType", help="Option Type")
        parser.add_argument("-r", "--strike-price", help="Strike Price")
        parser.add_argument("-s", "--symbol", help="Stock/Instrument Code", required=True)
        parser.add_argument("-i", "--index", help="Index", action='store_true')
        parser.add_argument("-f", "--futures", help="Futures", action='store_true')
        parser.add_argument("-g", "--no-graph", help="Graph Not Required", action='store_true')
        return

    # Entry to command execution
    def main(self, args):
        from_date = Utils.get_date_from_string(args.beginDate)
        to_date = Utils.get_date_from_string(args.endDate)

        try:
            expiry_date = None if args.expiryDate is None else Utils.get_date_from_string(args.expiryDate)
        except ValueError:
            expiry_month_year = Utils.get_month_year_from_string(args.expiryDate)
            expiry_date = list(get_expiry_date(year=expiry_month_year.year, month=expiry_month_year.month))[0]

        strike_price = None if args.strike_price is None else int(args.strike_price)
        if args.optionType is None:
            data = get_history(symbol=args.symbol, start=from_date, end=to_date, index=args.index, futures=args.futures,
                               expiry_date=expiry_date, strike_price=strike_price)
        else:
            data = get_history(symbol=args.symbol, start=from_date, end=to_date, index=args.index, futures=args.futures,
                               expiry_date=expiry_date, option_type=args.optionType, strike_price=strike_price)

        print(data)
        if args.no_graph is False and len(data) > 0:
            Utils.plot_graph(args.plotType, data)
