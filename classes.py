class Stock:
    def __init__(self, name, buy_percent, curr_percent):
        self._name = name
        self._buy_percent = buy_percent
        self._curr_percent = curr_percent
    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_buy_percent(self):
        return self._buy_percent

    def set_buy_percent(self, buy_percent):
        self._buy_percent = buy_percent

    def get_curr_percent(self):
        return self._curr_percent

    def set_curr_percent(self, curr_percent):
        self._curr_percent = curr_percent

    def display_info(self):
        print(f"Stock: {self._name}")
        print(f"Buy Percentage: {self._buy_percent}%")
        print(f"Current Percentage: {self._curr_percent}%")