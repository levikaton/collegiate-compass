import requests
import json

def search_schools(api_key, school_name):
    base_url = 'https://api.data.gov/ed/collegescorecard/v1/'
    endpoint = 'schools'
    
    params = {
        'api_key': api_key,
        'school.name': school_name,
    }

    response = requests.get(f'{base_url}{endpoint}', params=params)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results')

        if results:
            schools_info = []

            for result in results:
                school_info = {}
                
                location_info = result.get('location')
                if location_info:
                    school_info['latitude'] = location_info.get('lat')
                    school_info['longitude'] = location_info.get('lon')

                latest_info = result.get('latest')
                if latest_info:
                    school_info['name'] = latest_info.get('school', {}).get('name', 'N/A')
                    school_info['zip_code'] = latest_info.get('school', {}).get('zip', 'N/A')
                    school_info['city'] = latest_info.get('school', {}).get('city', 'N/A')
                    school_info['state'] = latest_info.get('school', {}).get('state', 'N/A')
                    school_info['address'] = latest_info.get('school', {}).get('address', 'N/A')
                    school_info['school_url'] = latest_info.get('school', {}).get('school_url', 'N/A')
                    school_info['online_only'] = latest_info.get('school', {}).get('online_only', 'N/A')

                    cost_info = latest_info.get('cost')
                    if cost_info:
                        school_info['booksupply_cost'] = cost_info.get('booksupply', 'N/A')
                        tuition_info = cost_info.get('tuition', {})
                        school_info['in_state_tuition'] = tuition_info.get('in_state', 'N/A')
                        school_info['out_of_state_tuition'] = tuition_info.get('out_of_state', 'N/A')

                    admissions_info = latest_info.get('admissions')
                    if admissions_info:
                        act_scores_info = admissions_info.get('act_scores', {}).get('midpoint', {})
                        school_info['act_midpoint_math'] = act_scores_info.get('math', 'N/A')
                        school_info['act_midpoint_english'] = act_scores_info.get('english', 'N/A')
                        school_info['act_midpoint_writing'] = act_scores_info.get('writing', 'N/A')
                        school_info['act_midpoint_cumulative'] = act_scores_info.get('cumulative', 'N/A')

                        sat_scores_info = admissions_info.get('sat_scores', {}).get('midpoint', {})
                        school_info['sat_midpoint_math'] = sat_scores_info.get('math', 'N/A')
                        school_info['sat_midpoint_writing'] = sat_scores_info.get('writing', 'N/A')
                        school_info['sat_midpoint_critical_reading'] = sat_scores_info.get('critical_reading', 'N/A')

                    programs_info = latest_info.get('programs')
                    if programs_info:
                        cip_4_digit_info = programs_info.get('cip_4_digit', [])
                        school_info['programs'] = []
                        for program in cip_4_digit_info:
                            credential_info = program.get('credential')
                            if credential_info and credential_info.get('level') == 3:
                                program_info = {
                                    'title': program.get('title', 'N/A'),
                                    'credential_level': credential_info.get('title', 'N/A')
                                }
                                school_info['programs'].append(program_info)

                schools_info.append(school_info)

            with open('schools_data.json', 'w') as json_file:
                json.dump(schools_info, json_file, indent=2)

        else:
            print(f"No results found for '{school_name}'.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    api_key = 'kK3BZnAbjkyuoZuB4BW2VapEPB7Z0giWOkm8uKb4'

    school_name = input("Enter the name of the school: ")

    search_schools(api_key, school_name)

if __name__ == "__main__":
    main()
