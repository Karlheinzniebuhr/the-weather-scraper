import re


class ConvertToSystem:
    supported_systems = ["metric"]
    round_to_decimals = 2
    extract_numbers_pattern = "\d*\.\d+|\d+"

    def __init__(self, system: str):
        if system not in self.supported_systems:
            raise ValueError('unit system not supported')
        else:
            self.system = system


    def temperature(self, temp_string: str):
        fahrenheit = float(re.findall(self.extract_numbers_pattern, temp_string)[0])
        if self.system == "metric":
            celsius = (fahrenheit - 32) * 5/9
            return round(celsius, self.round_to_decimals)
        else:
            return fahrenheit


    def dew_point(self, dew_point: str):
        fahrenheit = float(re.findall(self.extract_numbers_pattern, dew_point)[0])
        if self.system == "metric":
            celsius = (fahrenheit - 32) * 5/9
            return round(celsius, self.round_to_decimals)
        else:
            return fahrenheit


    def humidity(self, humidity: str):
        humidity = float(re.findall(self.extract_numbers_pattern, humidity)[0])
        return humidity

    
    def speed(self, speed_string):
        mph = float(re.findall(self.extract_numbers_pattern, speed_string)[0])
        if self.system == "metric":
            kmh = mph * 1.609
            return round(kmh, self.round_to_decimals)
        else:
            return mph

    
    def pressure(self, pressure_string):
        inhg = float(re.findall(self.extract_numbers_pattern, pressure_string)[0])
        if self.system == "metric":
            hpa = inhg * 33.86389
            return round(hpa, self.round_to_decimals)
        else:
            return inhg
    
    def precipitation(self, precip_string):
        inches = float(re.findall(self.extract_numbers_pattern, precip_string)[0])
        if self.system == "metric":
            mm = inches * 25.4
            return round(mm, self.round_to_decimals)
        else:
            return inches


    def uv(self, uv_string):
        measure = float(re.findall(self.extract_numbers_pattern, uv_string)[0])
        return measure


    def solar(self, solar_string):
        measure = float(re.findall(self.extract_numbers_pattern, solar_string)[0])
        return measure


    def convert_dict_list(self, dict_list: list):
        converted_dict_list = []
        for dict in dict_list:
            converted_dict = {}
            for key, value in dict.items():
                if key == 'Date':
                    converted_dict['Date'] = value
                if key == 'Time':
                    converted_dict['Time'] = value
                if key ==  'Temperature':
                    converted_dict['Temperature'] = self.temperature(value)
                if key ==  'Dew_Point':
                    converted_dict['Dew_Point'] = self.dew_point(value)
                if key ==  'Humidity':
                    converted_dict['Humidity'] = self.humidity(value)
                if key ==  'Wind':
                    converted_dict['Wind'] = value
                if key ==  'Speed':
                    converted_dict['Speed'] = self.speed(value)
                if key ==  'Gust':
                    converted_dict['Gust'] = self.speed(value)
                if key ==  'Pressure':
                    converted_dict['Pressure'] = self.pressure(value)
                if key ==  'Precip_Rate':
                    converted_dict['Precip_Rate'] = self.precipitation(value)
                if key ==  'Precip_Accum':
                    converted_dict['Precip_Accum'] = self.precipitation(value)
                if key ==  'UV':
                    converted_dict['UV'] = self.uv(value)
                if key ==  'Solar':
                    converted_dict['Solar'] = self.solar(value)

            converted_dict_list.append(converted_dict)

        return converted_dict_list