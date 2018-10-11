from bs4 import BeautifulSoup
import re, sys # peanutbutter cup


def get_score_list(filename):
    try:
        with open(filename, 'r') as file:
            soup = BeautifulSoup(file, 'html.parser')
    except IOError as e:
        print("Issue reading file {}\n{}".format(filename, e))
        sys.exit()
    
    odd_divs = soup.findAll("tr", {"class": "esr-odd-row nw-progress-row"})
    even_divs = soup.findAll("tr", {"class": "esr-even-row nw-progress-row"})
    divs = odd_divs + even_divs
    
    n_start = '<div class="esr-nw-weight-data" id="esr-nw-weight-data-id">'
    n_end = '%</div>'
    networkhealth = re.findall(n_start+'(.*)'+n_end, str(soup))[0]
    
    score_list = []
    for div in divs:
        result_group = re.findall('">(.*)</', str(div))
        score_list.append(result_group)
    
    return score_list, networkhealth

def get_score_dict(filename):
    score_list, ns = get_score_list(filename)
    score_dict = {}
    for score in score_list:
        score_dict[score[0]] = score[2]
    return score_dict, ns


def main():
    with open('THISNEEDSTOBECHANGED_Filenameoftestfile') as file:
        soup = BeautifulSoup(file, 'html.parser')
    #print(str(soup)[:15000])
    
    return 0

if __name__ == "__main__":
    sys.exit(main())