# requires extract_user_data_from_wikiloves_db.py to be run first
# get some user statistics (into bins)
# total users
# total images
# number of users by number of competitions
# number of users by number of WLM-competitions
# number of users by number of WLE-competitions
# WLE/WLM registered users by number of competitions
import json
from collections import Counter

def display_counter_dict(counter_dict, delimiter="\t"):
    '''Visualise the dict of coutners as a tsv table.'''
    max_counter = max({label:max(count) for label, count in counter_dict.items()}.values())
    cols = list(counter_dict.keys())
    outdata = f'counter{delimiter}{delimiter.join(cols)}\n'
    for num in range(1, max_counter+1):
        vals = [str(counter_dict[col][num]) for col in cols]
        outdata += f'{num}{delimiter}{delimiter.join(vals)}\n'
    return outdata

def display_max_val(d, label, delimiter="\t"):
    '''Identify the dictionary entries with the highest value and output them, and the value.'''
    temp = max(d.values())
    keys = [key for key in d if d[key] == temp]
    output = f'{label}:{delimiter}{"|".join(keys)}{delimiter}{temp}'
    return output


with open("db_users.json", encoding='utf-8') as f:
    data = json.load(f)

# number of users ordered by how many competitions they have participated in
users_by_comp_number = {'all':Counter(), 'wlm':Counter(), 'wle':Counter()}
# number of newly registered users (during wle/wlm) ordered by number of joined competitions
new_regs_by_comp_number = {'all':Counter(), 'wlm':Counter(), 'wle':Counter()}
# total wlm/wle uploads by user registered during a wle/wlm
new_reg_total = 0
# total wlm/wle uploads by any user
all_total = 0
# competitions in the data
comps = set()

for user, user_data in data.items():
    comps.update(user_data.get('competitions'))
    comp_num = len(user_data.get('competitions'))
    wlm_comps = sum(1 if c.startswith('monument') else 0 for c in user_data.get('competitions'))
    wle_comps = sum(1 if c.startswith('earth') else 0 for c in user_data.get('competitions'))
    wlm_reg = user_data.get('recruited') and user_data.get('recruited').startswith('monument')
    wle_reg = user_data.get('recruited') and user_data.get('recruited').startswith('earth')
    data[user]['newbie'] = wlm_reg or wle_reg  # 'recruited' but only considering wle/wlm
    users_by_comp_number.get('all')[comp_num] += 1
    users_by_comp_number.get('wlm')[wlm_comps] += 1
    users_by_comp_number.get('wle')[wle_comps] += 1
    all_total += user_data.get('count')
    if wlm_reg or wle_reg:
        new_regs_by_comp_number.get('all')[comp_num] += 1
        new_reg_total += user_data.get('count')
    if wlm_reg:
        new_regs_by_comp_number.get('wlm')[wlm_comps] += 1
    if wle_reg:
        new_regs_by_comp_number.get('wle')[wle_comps] += 1

# display results
print("General stats")
total_comps = sum(1 if c.startswith('monument') or c.startswith('earth') else 0 for c in comps)
print(f"total Sweden comps (only wle/wlm):\t{total_comps}")
print(f"total uploads (only wle/wlm):\t{all_total}")
print(f"total uploads (only wle/wlm) by user registered during a wle/wlm:\t{new_reg_total}")

print("----")
print("number of users ordered by how many competitions they have participated in:")
print(display_counter_dict(users_by_comp_number))

print("----")
print("number of newly registered users (during wle/wlm) ordered by how"
      " many competitions they have participated in:")
print(display_counter_dict(new_regs_by_comp_number))

# analyse individuals
comps_by_user = {}
comps_by_user_new = {}
uploads_by_user = {}
uploads_by_user_new = {}
for user, user_data in data.items():
    if user_data.get('newbie'):
        comps_by_user_new[user] = len(user_data.get('competitions'))
        uploads_by_user_new[user] = user_data.get('count')
    comps_by_user[user] = len(user_data.get('competitions'))
    uploads_by_user[user] = user_data.get('count')

# output results
print(display_max_val(comps_by_user, "Most competitions"))
print(display_max_val(uploads_by_user, "Most images"))
print(display_max_val(comps_by_user_new, "Most competitions by wle/wlm registrant"))
print(display_max_val(uploads_by_user_new, "Most images by wle/wlm registrant"))
