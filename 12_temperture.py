class TemperatreConverter:
    @staticmethod
    def celsius_to_fahrenheit(c):
        return (c * 9/5) + 32
print(TemperatreConverter.celsius_to_fahrenheit(20))