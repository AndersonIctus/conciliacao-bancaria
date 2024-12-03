from datetime import datetime
import calendar

class DataHelper:
    @staticmethod
    def get_data_extensao(date_reference: datetime = datetime.now()) -> str:
        """
        Retorna a data no formato <ANO>_<MES>_<MES POR EXTENSO>.
        
        :return: Uma string formatada no padrão <ANO>_<MES>_<MES POR EXTENSO>.
        """
        # Extrai ano, mês (número) e mês por extenso
        ano = date_reference.year
        mes = date_reference.month
        mes_por_extenso = calendar.month_name[mes]  # Nome do mês em inglês
        mes_por_extenso_pt = {
            "January": "JAN", "February": "FEV", "March": "MAR",
            "April": "ABR", "May": "MAI", "June": "JUN",
            "July": "JUL", "August": "AGO", "September": "SET",
            "October": "OUT", "November": "NOV", "December": "DEZ"
        }[mes_por_extenso]

        # Formata a string no padrão desejado
        result = f"{ano}_{mes:02d}_{mes_por_extenso_pt}"
        return result
