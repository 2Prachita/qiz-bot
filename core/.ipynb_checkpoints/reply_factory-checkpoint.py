
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST, TOTAL_QUESTIONS, NUMBER_OF_OPTIONS

def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return([error])

    next_question, next_question_id, options = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
        bot_responses.append(options)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''

    if(not current_question_id):
        return True, ""

    try:
        option_no = ord(answer.upper()) - 65
    except:
        return False, str("Please enter a single character")
    
    user_answer = str(PYTHON_QUESTION_LIST[current_question_id-1]['options'][option_no])
    actual_answer = str(PYTHON_QUESTION_LIST[current_question_id-1]['answer'])
    correct_ans_count = session.get("correct_ans_count", 0)
    if user_answer == actual_answer:
        correct_ans_count += 1
        
    try:
        session["correct_ans_count"] = correct_ans_count
        session["user_answer"] = user_answer
        session.save()
    except:
        return False, str("Answer not saved re-enter the answer")
    
    return True,""

def generate_question(question_id):
    '''
    Returns the question and its options from the PYTHON_QUESTION_LIST based on the question_id.
    '''
    next_question = PYTHON_QUESTION_LIST[question_id]['question_text']
    option = ""
    for option_no in range(0,NUMBER_OF_OPTIONS):
        option = option + chr(65+option_no) + ".  " + str(PYTHON_QUESTION_LIST[question_id]['options'][option_no])
        option += "  \n\n"
        
    return next_question, option


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id == -1:
        next_question_id = -1
        next_question = None
        options = None
    else:
        if current_question_id == 0 or current_question_id == None:
            next_question_id = 1
            current_question_id = 0
        elif current_question_id < TOTAL_QUESTIONS-1:
            next_question_id = current_question_id + 1
        elif current_question_id == TOTAL_QUESTIONS-1:
            next_question_id = -1
        next_question, options = generate_question(current_question_id)

    return next_question, next_question_id, options


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    correct_ans_count = session.get("correct_ans_count")
    return("You scored a %s out of %s on python programming skils test." % (correct_ans_count,TOTAL_QUESTIONS))
