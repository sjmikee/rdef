# VirusTotal API response parser


class vt_response_parser():
    '''The following class will parse all releavant data in the project
       that was returned via the VT http/https requests'''

    def last_analysis_stats(self, jsondata):
        '''Function that returns last analysis attribute from the Json data VT API'''
        return [jsondata["data"]["attributes"]["last_analysis_stats"][i] for i in jsondata["data"]["attributes"]["last_analysis_stats"]]
