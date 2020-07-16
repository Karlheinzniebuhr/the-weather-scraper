import re


class ConvertToSystem:
    supported_systems = ["metric", "imperial"]
    round_to_decimals = 2
    extract_numbers_pattern = "\d*\.\d+|\d+"

    def __init__(self, system: str):
        if system not in self.supported_systems:
            raise ValueError('unit system not supported')
        else:
            self.system = system

    def temperature(self, temp_string: str):
        try:
            fahrenheit = float(re.findall(self.extract_numbers_pattern, temp_string)[0]) if temp_string else 'NA'
            if self.system == "metric":
                celsius = (fahrenheit - 32) * 5/9
                return round(celsius, self.round_to_decimals)
            else:
                return fahrenheit

        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'
            
    def dew_point(self, dew_point_string: str):
        try:
            fahrenheit = float(re.findall(self.extract_numbers_pattern, dew_point_string)[0]) if dew_point_string else 'NA'
            if self.system == "metric":
                celsius = (fahrenheit - 32) * 5/9
                return round(celsius, self.round_to_decimals)
            else:
                return fahrenheit
            
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def humidity(self, humidity_string: str):
        try:
            humidity = float(re.findall(self.extract_numbers_pattern, humidity_string)[0]) if humidity_string else 'NA'
            return humidity
        
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def speed(self, speed_string: str):
        try:
            mph = float(re.findall(self.extract_numbers_pattern, speed_string)[0]) if speed_string else 'NA'
            if self.system == "metric":
                kmh = mph * 1.609
                return round(kmh, self.round_to_decimals)
            else:
                return mph

        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def pressure(self, pressure_string: str):
        try:
            inhg = float(re.findall(self.extract_numbers_pattern, pressure_string)[0]) if pressure_string else 'NA'
            if self.system == "metric":
                hpa = inhg * 33.86389
                return round(hpa, self.round_to_decimals)
            else:
                return inhg
                
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'
    
    def precipitation(self, precip_string: str):
        try:
            inches = float(re.findall(self.extract_numbers_pattern, precip_string)[0]) if precip_string else 'NA'
            if self.system == "metric":
                mm = inches * 25.4
                return round(mm, self.round_to_decimals)
            else:
                return inches
                
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def uv(self, uv_string: str):
        try:
            measure = float(re.findall(self.extract_numbers_pattern, uv_string)[0]) if uv_string else 'NA'
            return measure
            
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def solar(self, solar_string: str):
        try:
            measure = float(re.findall(self.extract_numbers_pattern, solar_string)[0]) if solar_string else 'NA'
            return measure
            
        except Exception as e:
            print(f'{e}! probably caused by an empty row in the data')
            return 'NA'

    def clean_and_convert(self, dict_list: list):
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