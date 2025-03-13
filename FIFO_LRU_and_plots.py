import random
import numpy as np
import matplotlib.pyplot as plt
import sys

pages = []  # declaring a list of pages that will contain all generated pages

def generator(number, range_stop, generated_pages):  # generator function
    generated_pages.clear()
    for i in range(number):  # adding generated pages to the list, specifying the range of page numbers
        generated_pages.append(random.randint(0, range_stop))

def stats(page_fault, number):  # function responsible for calculating statistical data for each algorithm
    page_fault_probability = page_fault/number
    page_fault_percentage = page_fault_probability * 100
    print("Total number of page faults are: " + str(page_fault))
    print("Page fault probability: " + str(page_fault_probability))
    print("Page fault percentage: " + str(round(page_fault_percentage, 2)))

# FIFO
def fifo(number, generated_pages):  # FIFO function for sorting for this algorithm
    print("\nFIFO")
    print("Generated pages:" + str(generated_pages))
    capacity = 4  # number of slots
    pf = 0
    list_of_pages = []  # list to store sorted pages
    queue = []  # auxiliary list to maintain page entry order
    for i in range(number):  # dividing the algorithm into two cases, first when the list is not yet full
        if len(list_of_pages) < capacity:  # checking if the number of pages is less than the number of available slots
            if generated_pages[i] not in list_of_pages:  # if the page is not in the list, add it to the end
                list_of_pages.append(generated_pages[i])
                pf += 1  # updating the page faults count on each replacement
                queue.append(generated_pages[i])  # second list storing the same pages but in order
        else:  # second case when the list is full
            if generated_pages[i] not in list_of_pages:  # if the page is not in the list, a replacement occurs
                val = queue[0]
                queue.remove(val)
                ind = list_of_pages.index(val)
                list_of_pages[ind] = generated_pages[i]
                queue.append(generated_pages[i])
                pf += 1
    print("Final FIFO list of pages: " + str(list_of_pages))
    stats(pf, number)  # calling the function that calculates statistics for this algorithm
    return pf  # returning the number of page faults

# LRU
def lru(number, generated_pages):
    print("\nLRU")
    capacity = 4
    pf = 0
    list_of_pages = []
    queue = []

    for i in range(number):  # similar to FIFO
        if len(list_of_pages) < capacity:
            if generated_pages[i] not in list_of_pages:
                list_of_pages.append(generated_pages[i])
                pf += 1
                queue.append(generated_pages[i])
        else:
            if generated_pages[i] not in list_of_pages:
                val = queue[0]
                queue.remove(val)
                ind = list_of_pages.index(val)
                list_of_pages[ind] = generated_pages[i]
                queue.append(generated_pages[i])
                pf += 1
            else:  # with the difference that when the page is already in the list
                val2 = queue.index(generated_pages[i])  # only the order in the queue changes
                del queue[val2]
                queue.append(generated_pages[i])  # the incoming page moves to the end of the queue, as it was used most recently
                                                # unlike FIFO, this option is considered

    print("Final LRU list of pages: " + str(list_of_pages))
    stats(pf, number)
    return pf

print("\nComparison of FIFO and LRU for a fixed page number range 0-10 and different number of pages")

# Obtaining data for plots
generator(10, 10, pages)  # generating required experiments
fifo_pg10 = fifo(10, pages)
lru_pg10 = lru(10, pages)

generator(25, 10, pages)
fifo_pg25 = fifo(25, pages)
lru_pg25 = lru(25, pages)

generator(50, 10, pages)
fifo_pg75 = fifo(50, pages)
lru_pg75 = lru(50, pages)

generator(100, 10, pages)
fifo_pg125 = fifo(100, pages)
lru_pg125 = lru(100, pages)

# Generating a bar chart for comparison
def plot_comparison_bar(data_fifo, data_lru, title, ylabel):  # function for automatically generating plots
    x = np.arange(len(data_fifo))
    width = 0.35

    fig, ax = plt.subplots()
    fifo_bars = ax.bar(x - width/2, data_fifo, width, label='FIFO')
    lru_bars = ax.bar(x + width/2, data_lru, width, label='LRU')

    ax.set_xlabel('Number of pages')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(['10', '25', '50', '100'])
    ax.legend()

    # adding labels to bars
    def add_labels(bars):
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points above the bar height
                        textcoords="offset points",
                        ha='center', va='bottom')

    add_labels(fifo_bars)
    add_labels(lru_bars)

    fig.tight_layout()

    plt.show()

# Generating plots for different experiments
plot_comparison_bar([fifo_pg10, fifo_pg25, fifo_pg75, fifo_pg125],
                    [lru_pg10, lru_pg25, lru_pg75, lru_pg125],
                    'Comparison of FIFO and LRU for a fixed page number range \n0-10 and different number of pages', 'Page Faults')
