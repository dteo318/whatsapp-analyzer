import datetime

def create_msg_lst(user_name_1, user_name_2, text_file):
    msg_lst1 = []
    msg_lst2 = []
    for line in text_file:
        if '{}:'.format(user_name_1) in line:
            msg_lst1.append(line[:-1])
        elif '{}:'.format(user_name_2) in line:
            msg_lst2.append(line[:-1])
    return msg_lst1, msg_lst2

def count_msgs(msg_lst):
    return len(msg_lst)

def count_words(user_name, msg_lst, msg_count):
    total_word_count = 0
    for msg in msg_lst:
        total_word_count += len(msg.split('{}: '.format(user_name))[1].split(' '))
    return round(total_word_count/msg_count, 2), total_word_count

def format_date_time(string):
    dt_portion = string.split(' - ')[0]
    d_portion = dt_portion.split(', ')[0].split('/')
    t_portion = dt_portion.split(', ')[1].split(' ')[0].split(':')
    if 'AM' in dt_portion:
        return datetime.datetime(int("20"+d_portion[2]), 
                                int(d_portion[0]), 
                                int(d_portion[1]),
                                int(t_portion[0]),
                                int(t_portion[1]),
                                )
    elif 'PM' in dt_portion and int(t_portion[0]) == 12:
        return datetime.datetime(int("20"+d_portion[2]), 
                                int(d_portion[0]), 
                                int(d_portion[1]),
                                0,
                                int(t_portion[1]),
                                )
    else:
        return datetime.datetime(int("20"+d_portion[2]), 
                                int(d_portion[0]), 
                                int(d_portion[1]),
                                (int(t_portion[0]) + 12),
                                int(t_portion[1]),
                                )

def avg_wait_for_reply(user_name_1, user_name_2, text_file):
    wait_durations = []
    waiting_reply = False
    user_waiting, first_msg_sent_time = None, None
    for line in text_file:
        try:
            if not waiting_reply:
                if '{}:'.format(user_name_1) in line:
                    user_waiting = user_name_1
                    first_msg_sent_time = format_date_time(line)
                    waiting_reply = True
                elif '{}:'.format(user_name_2) in line:
                    user_waiting = user_name_2
                    first_msg_sent_time = format_date_time(line)
                    waiting_reply = True
            elif waiting_reply:
                if '{}:'.format(user_waiting) not in line:
                    tdelta = format_date_time(line) - first_msg_sent_time
                    wait_durations.append(tdelta)
                    waiting_reply = False
                    user_waiting, first_msg_sent_time = None, None
        except:
            continue
    total_wait_duration = datetime.timedelta(seconds=0)
    for d in wait_durations:
        total_wait_duration += d
    return ((total_wait_duration) / len(wait_durations))

def count_first_texts(user_name_1, user_name_2, text_file):
    first_msgs = []
    user1_first_msgs = []
    user1_num_first_msgs = 0
    user2_first_msgs = []
    user2_num_first_msgs = 0
    last_msg_sent_time = None
    for line in text_file:
        try:
            if not last_msg_sent_time:
                last_msg_sent_time = format_date_time(line)
            else:
                tdelta = format_date_time(line) - last_msg_sent_time
                if tdelta > datetime.timedelta(hours=3):
                    first_msgs.append(line)
                last_msg_sent_time = format_date_time(line)               
        except:
            continue
    for msg in first_msgs:
        if user_name_1 in msg:
            user1_num_first_msgs += 1
            user1_first_msgs.append(msg)
        elif user_name_2 in msg:
            user2_num_first_msgs += 1
            user2_first_msgs.append(msg)
    if user1_num_first_msgs > user2_num_first_msgs:
        return user_name_1, user1_num_first_msgs, user1_first_msgs, len(first_msgs)
    else:
        return user_name_2, user2_num_first_msgs, user2_first_msgs, len(first_msgs)

def days_chat(text_file):
    days_msg_count = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0,
        5 : 0,
        6 : 0,
        7 : 0
    }
    for line in text_file:
        try:
            day_msg_sent = format_date_time(line).isoweekday()
            days_msg_count[day_msg_sent] = days_msg_count.get(day_msg_sent) + 1
        except:
            continue
    
    return days_msg_count

def hour_chat(text_file):
    hour_msg_count = {

    }
    for line in text_file:
        try: 
            dt_h = format_date_time(line).hour
            hour_msg_count[dt_h] = hour_msg_count.get(dt_h, 0) + 1
        except:
            continue

    return hour_msg_count

def month_chat(text_file):
    month_msg_count = {

    }
    for line in text_file:
        try: 
            dt_m = format_date_time(line).month
            month_msg_count[dt_m] = month_msg_count.get(dt_m, 0) + 1
        except:
            continue

    return month_msg_count

def words_used(username, user_msg_list):
    words_used = {}
    for line in user_msg_list:
        msg = line.split('{}: '.format(username))[1]
        words_in_msg = msg.split(' ')
        for word in words_in_msg:
            words_used[word] = words_used.get(word, 0) + 1
    return {k: v for k, v in sorted(words_used.items(), key=lambda item: item[1])}

def filter_stopwords(words_dict):
    new_word_dict = {}
    stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", 
                 "again", "against", "all", "almost", "alone", "along", "already", "also",
                 "although","always","am","among", "amongst", "amoungst", "amount",  "an", 
                 "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", 
                 "are", "around", "as",  "at", "back","be","became", "because","become","becomes",
                 "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", 
                 "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", 
                 "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", 
                 "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", 
                 "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", 
                 "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", 
                 "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", 
                 "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", 
                 "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", 
                 "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", 
                 "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", 
                 "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", 
                 "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", 
                 "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", 
                 "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", 
                 "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", 
                 "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", 
                 "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", 
                 "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", 
                 "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", 
                 "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", 
                 "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", 
                 "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", 
                 "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", 
                 "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", 
                 "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", 
                 "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", 
                 "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", 
                 "your", "yours", "yourself", "yourselves", "the", "i", "like", "just", "okay", "oh", "cause", 
                 "its", "know", "ye", "it's", "cos", "u","really", "i'm", "don't", "think", "it's", "ok", "thanks", "cuz", "ya", "damn", "la", "ah"]
    for word, num in words_dict.items():
        if word.lower() not in stopwords:
            new_word_dict[word] = num
    return new_word_dict

# --- EDIT THIS: Replace the None with the file name of the WhatsApp .txt file eg. (with quotes) 'WhatsApp Chat with Henry.txt'
text_file_name = None 

with open(text_file_name, 'r') as chat:
    username1 = None # --- Name of first chatee, follow the name within the .txt file
    username2 = None # --- Name of second chatee, follow the name within the .txt file
    convo_list = list(chat)[1:]
    
    # When WhatsApp convo started and ended
    first_msg_date = format_date_time(convo_list[0])
    last_msg_date = format_date_time(convo_list[-1])
    
    # Creating each user's msg list and calculating num of msgs sent 
    user1_msg_lst, user2_msg_lst = create_msg_lst(username1, username2, convo_list)
    user1_msg_num = count_msgs(user1_msg_lst)
    user2_msg_num = count_msgs(user2_msg_lst)
    total_msg_num = count_msgs(user1_msg_lst+user2_msg_lst)
    
    # Analysis of the num words in each msg 
    user1_msg_avg_word_count, user1_msg_total_word_count = count_words(username1, user1_msg_lst, user1_msg_num)
    user2_msg_avg_word_count, user2_msg_total_word_count = count_words(username2, user2_msg_lst, user2_msg_num)
    
    # Analysis of the time between msgs and who started convos 
    avg_waiting_time = avg_wait_for_reply(username1, username2, convo_list)
    most_convo_starters, num_convo_starters, convo_starters, total_convos = count_first_texts(username1, username2, convo_list)
    
    # Analysis of the time, days, and months, and the num of msgs sent
    days = days_chat(convo_list)
    hours = hour_chat(convo_list)
    month = month_chat(convo_list)
    
    # Analysis of the words used by each user 
    user1_words = words_used(username1, user1_msg_lst)
    user2_words = words_used(username2, user2_msg_lst)
    user1_words_no_stopwords = filter_stopwords(user1_words)
    user2_words_no_stopwords = filter_stopwords(user2_words)

# Select what data to print
print(hours)
