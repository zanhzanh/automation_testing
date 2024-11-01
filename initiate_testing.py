from browser_manipulation import Browser
import excel_manipulation

import threading
import numpy as np

from typing import List
from queue import Queue

def clean_data(num_split: int, questions: list, test_results) -> List[np.ndarray]:
    if not test_results:
        return np.array_split(questions, num_split)

    cleaned_questions = [
        q if (isinstance(r, str) and r != "Pass") else ""
        for q, r in zip(questions, test_results)
    ]

    return np.array_split(cleaned_questions, num_split)


def start_testing(username: str, password: str, url: str, path: str, file_name: str, test_results_column: str, number_tabs: str) -> None:
    all_data, questions, test_results = excel_manipulation.extract_data(test_results_column, file_name, path)

    number_tabs_int = int(number_tabs)

    questions_chunks = clean_data(number_tabs_int, questions, test_results)

    threads = []
    result_queue = Queue()
    for i in range(number_tabs_int):
        thread = threading.Thread(target=test_cycle, args=(username, password, url, questions_chunks[i], i, result_queue))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    results = []
    while not result_queue.empty():
        results.append(result_queue.get())

    sorted_data = sorted(results, key=lambda x: x[0])

    combined_list = [text for _, text_list in sorted_data for text in text_list]

    for i in range(len(questions)):
        if not isinstance(questions[i], str):
            combined_list.insert(i, '')

    excel_manipulation.create_new_file(all_data, combined_list, file_name, path)


def test_cycle(username: str, password: str, url: str, questions: list, thread_id: int, result_queue):
    browser = Browser('geckodriver.exe')
    browser.open_page(url)
    browser.login(username, password)
    browser.stop_voice()

    answers_to_text = []

    for q in range(len(questions)):
        if questions[q] != '':
            browser.ask_question(questions[q])
            answer = browser.get_answer()
            answers_to_text.append(answer.text)
            browser.reset_chat()
        else:
            answers_to_text.append('')

    browser.close_browser()
    result_queue.put((thread_id, answers_to_text))
