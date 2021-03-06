import os
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import _pickle as cPickle
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import cm
from scipy.ndimage.filters import gaussian_filter1d
from corextopic import corextopic as ct
from datetime import datetime
import dateutil.parser
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import FormatStrFormatter


def values_in_different_datasets(df_with_topics, selected_technology, dict_anchor_words):
    
    list_values = list(dict_anchor_words.keys())
    list_values_int = []
    for i in list_values:
        list_values_int.append(list(dict_anchor_words.keys()).index(i))
    
    df_with_topics_NEWS = df_with_topics[df_with_topics['dataset'] == 'NEWS']
    df_with_topics_NEWS = df_with_topics_NEWS[df_with_topics_NEWS[selected_technology] == True]
    df_with_topics_sum_NEWS = df_with_topics_NEWS[[c for c in df_with_topics_NEWS.columns if c in list_values_int]]
    df_with_topics_sum_NEWS.columns = list_values
    df_sum_NEWS = df_with_topics_sum_NEWS.sum(numeric_only=True)
    series_perc_selected_tech_NEWS = df_sum_NEWS.apply(lambda x: x / len(df_with_topics_sum_NEWS) * 100)

    df_with_topics_ETHICS = df_with_topics[df_with_topics['dataset'] == 'ETHICS']
    df_with_topics_ETHICS = df_with_topics_ETHICS[df_with_topics_ETHICS[selected_technology] == True]
    df_with_topics_sum_ETHICS = df_with_topics_ETHICS[[c for c in df_with_topics_ETHICS.columns if c in list_values_int]]
    df_with_topics_sum_ETHICS.columns = list_values
    df_sum_ETHICS = df_with_topics_sum_ETHICS.sum(numeric_only=True)    
    series_perc_selected_tech_ETHICS = df_sum_ETHICS.apply(lambda x: x / len(df_with_topics_sum_ETHICS) * 100)

    df_with_topics_TECH = df_with_topics[df_with_topics['dataset'] == 'TECH']
    df_with_topics_TECH = df_with_topics_TECH[df_with_topics_TECH[selected_technology] == True]
    df_with_topics_sum_TECH = df_with_topics_TECH[[c for c in df_with_topics_TECH.columns if c in list_values_int]]
    df_with_topics_sum_TECH.columns = list_values
    df_sum_TECH = df_with_topics_sum_TECH.sum(numeric_only=True)    
    series_perc_selected_tech_TECH = df_sum_TECH.apply(lambda x: x / len(df_with_topics_sum_TECH) * 100)   
    
    df_perc_selected_tech_NEWS = series_perc_selected_tech_NEWS.to_frame()
    df_perc_selected_tech_ETHICS = series_perc_selected_tech_ETHICS.to_frame()
    df_perc_selected_tech_TECH = series_perc_selected_tech_TECH.to_frame()

    df_perc_selected_tech_all = pd.concat([df_perc_selected_tech_NEWS, df_perc_selected_tech_ETHICS.reindex(df_perc_selected_tech_NEWS.index)], axis=1)
    df_perc_selected_tech_all = pd.concat([df_perc_selected_tech_all, df_perc_selected_tech_TECH.reindex(df_perc_selected_tech_all.index)], axis=1)

    df_perc_selected_tech_all.columns = ['NEWS','ETHICS','TECH']
    
    c = {"NEWS": "#1f77b4", "ETHICS": "#ff7f0e", "TECH": "#2ca02c"}

    plt.rcParams.update({'font.size': 20})
    ax = df_perc_selected_tech_all.plot(kind='bar', figsize=(10,10), color=c, width = 0.75)
    ax.set_ylabel("%")
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    plt.title("Values for "+str(selected_technology))
    
    print("Number articles NEWS: "+str(len(df_with_topics_NEWS)))
    print("Number articles ETHICS: "+str(len(df_with_topics_ETHICS)))
    print("Number articles TECH: "+str(len(df_with_topics_TECH)))


def values_in_different_groups(df_with_topics, dict_anchor_words, selected_dataset):
    
    
        
    df_with_topics_field = df_with_topics.loc[df_with_topics['dataset'] == selected_dataset]
        

        
    df_sum_dataset_short = df_with_topics_field.sum(numeric_only=True)
        

    df_sum_dataset_short = df_sum_dataset_short.drop(['IoT', 'AI'])
        

        
    series_perc_dataset_short = df_sum_dataset_short.apply(lambda x: x / len(df_with_topics_field) * 100)
    series_perc_dataset_short = series_perc_dataset_short[:len(dict_anchor_words)]

    counter = 0
    for value, keywords in dict_anchor_words.items():
        series_perc_dataset_short = series_perc_dataset_short.rename({counter: value})
        counter = counter + 1
        
    series_perc_dataset_short = series_perc_dataset_short.sort_values(ascending = False)
        
    series_perc_dataset_short = series_perc_dataset_short.rename(selected_dataset)
    df_perc_dataset_short = series_perc_dataset_short.to_frame()

        
    c = {"NEWS": "#1f77b4", "ETHICS": "#ff7f0e", "TECH": "#2ca02c"}
        
    plt.rcParams.update({'font.size': 16})
    ax = df_perc_dataset_short.plot(kind='barh', figsize=(10,10),
                                        color=c)
    ax.set_xlabel("%")
    plt.title("Distribution of values")
    plt.gca().invert_yaxis()

def topic_int_or_string(Topic_selected, dict_anchor_words):
    
    if type(Topic_selected) == str:
        list_keys = list(dict_anchor_words.keys())
        Topic_selected_number = list_keys.index(Topic_selected)
    else:
        Topic_selected_number = Topic_selected
        
    return Topic_selected_number

def create_vis_frequency_values(df_with_topics, dict_anchor_words):
    
    # list values and list values int
    name_values = list(dict_anchor_words.keys())
    list_values_int = []
    for i in name_values:
        integ = topic_int_or_string(i, dict_anchor_words)
        list_values_int.append(integ)

   
    df_with_topics_sum_dataset_short = df_with_topics[[c for c in df_with_topics.columns if c in list_values_int]]
    df_with_topics_sum_dataset_short.columns = name_values
    df_sum_dataset_short = df_with_topics_sum_dataset_short.sum(numeric_only=True)
    series_perc_dataset_short = df_sum_dataset_short.apply(lambda x: x / len(df_with_topics_sum_dataset_short) * 100)
    series_perc_dataset_short = series_perc_dataset_short.sort_values(ascending=False)
    
    df_perc_dataset_short = series_perc_dataset_short.to_frame()
    #df_perc_dataset_short.columns = ["Percentage of documents mentioning each value"]
    

    
#    c = {"NEWS": "#1f77b4", "ETHICS": "#ff7f0e", "TECH": "#2ca02c", "LEGAL": "#d62728"}
    
    plt.rcParams.update({'font.size': 16})
    ax = df_perc_dataset_short.plot(kind='bar', figsize=(6,6),legend=False)#,
#                                    color=c)
    ax.set_ylabel("%")
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
    #plt.show()

def create_vis_values_over_time(df_with_topics, dict_anchor_words, resampling, values_to_include_in_visualisation, smoothing, max_value_y):
    
    copy_df_with_topics = df_with_topics.copy()
    copy_dict_anchor_words = dict_anchor_words.copy()
    
    df_with_topics_freq = copy_df_with_topics.set_index('date').resample(resampling).size().reset_index(name="count")
    df_with_topics_freq = df_with_topics_freq.set_index('date')

    df_frequencies = copy_df_with_topics.set_index('date')
    df_frequencies = df_frequencies.resample(resampling).sum()
       
    list_topics = list(range(len(copy_dict_anchor_words)))
    df_frequencies = df_frequencies[list_topics]
    
    df_frequencies = df_frequencies[list_topics].div(df_with_topics_freq["count"], axis=0)
    combined_df = pd.concat([df_frequencies, df_with_topics_freq], axis=1)
    combined_df = combined_df.fillna(0)
    
    x = pd.Series(combined_df.index.values)
    x = x.dt.to_pydatetime().tolist()

    x = [ z - relativedelta(years=1) for z in x]

    
    name_values = list(copy_dict_anchor_words.keys())
    
    combined_df[list_topics] = combined_df[list_topics] * 100
    combined_df.columns = name_values + ["count"]
       
    if not values_to_include_in_visualisation:
        values_to_include_in_visualisation = name_values

    sigma = (np.log(len(x)) - 1.25) * 1.2 * smoothing

    print(values_to_include_in_visualisation)

    fig, ax1 = plt.subplots()
    for value in values_to_include_in_visualisation:
            ysmoothed = gaussian_filter1d(combined_df[value].tolist(), sigma=sigma)
            ax1.plot(x, ysmoothed, label=str(value), linewidth=2)

    
    ax1.set_xlabel('Time', fontsize=12, fontweight="bold")
    ax1.set_ylabel('Percentage of documents addressing each value \n per unit of time (lines)  (%)', fontsize=12, fontweight="bold")
    ax1.legend(prop={'size': 10})
    
    timestamp_0 = x[0]
    timestamp_1 = x[1]
    

    #width = (time.mktime(timestamp_1.timetuple()) - time.mktime(timestamp_0.timetuple())) / 86400 *.8
    width = (timestamp_1 - timestamp_0).total_seconds() / 86400 * 0.8
       
    ax2 = ax1.twinx()
    ax2.bar(x, combined_df["count"].tolist(), width=width, color='gainsboro')
    ax2.set_ylabel('Number of documents in the dataset \n per unit of time (bars)', fontsize=12, fontweight="bold")
    
    ax1.set_zorder(ax2.get_zorder()+1)
    ax1.patch.set_visible(False)
    
    ax1.set_ylim([0,max_value_y])
    

    fig.tight_layout() 
    plt.figure(figsize=(20,14), dpi= 400)
    
    #max_value_y = 100
    
    

    plt.rcParams["figure.figsize"] = [12,6]
    plt.show()
    
def coexistence_values(df_with_topics, dict_anchor_words, resampling, values_selected, smoothing, max_value_y):

    copy_df_with_topics = df_with_topics.copy()
    copy_dict_anchor_words = dict_anchor_words.copy()


    list_columns = copy_df_with_topics.columns.tolist()
    list_topics = list(copy_dict_anchor_words.keys())
    
    index = list_columns.index(0)

    counter = 0
    for i in list_columns:
        if counter >= index and counter < (len(list_topics) + index):
            list_columns[counter]=list_topics[counter - index]
        counter += 1
    
    copy_df_with_topics.columns = list_columns
    
    df_with_topics_freq_value_0 = copy_df_with_topics[[values_selected[0], 'date']].set_index('date').resample(resampling).size().reset_index(name="count")
    df_with_topics_freq_value_0 = df_with_topics_freq_value_0.set_index('date')
    
    df_with_topics_selected_topics = copy_df_with_topics[values_selected]
    list_counts = df_with_topics_selected_topics.sum(axis=1).tolist()
    
    counter = 0
    for i in list_counts:
        if i == len(values_selected):
            list_counts[counter] = 1
        else:
            list_counts[counter] = 0
        counter += 1
       
    df_with_topics_sum = copy_df_with_topics[["date"]]
    df_with_topics_sum = df_with_topics_sum.set_index('date')
    
    df_with_topics_sum['all_values_named'] = pd.Series(list_counts, index=df_with_topics_sum.index)
    
    df_with_topics_sum = df_with_topics_sum.resample(resampling).sum()
    
    df_with_topics_selected_topic = df_with_topics_sum.div(df_with_topics_freq_value_0["count"], axis=0)
    df_with_topics_selected_topic = df_with_topics_selected_topic.fillna(0)
    
    x = pd.Series(df_with_topics_selected_topic.index.values)
    x = x.dt.to_pydatetime().tolist()

    df_with_topics_selected_topic = df_with_topics_selected_topic * 100

    sigma = (np.log(len(x)) - 1.25) * 1.2 * smoothing

    fig, ax1 = plt.subplots()
    for word in df_with_topics_selected_topic:
        ysmoothed = gaussian_filter1d(df_with_topics_selected_topic[word].tolist(), sigma=sigma)
        ax1.plot(x, ysmoothed, linewidth=2)
        
        
        ax1.set_xlabel('Time', fontsize=12, fontweight="bold")
    
    
    ax1.set_ylabel('Percentage of articles mentioning \n '+str(values_selected[0])+' also mentioning \n '+str(values_selected[1])+ ' (% of documents)', fontsize=12, fontweight="bold")
    ax1.legend(prop={'size': 8})
    
    ax1.set_ylim([0,max_value_y])
    
    fig.tight_layout() 
    plt.figure(figsize=(20,14), dpi= 400)

    plt.rcParams["figure.figsize"] = [12,6]
    plt.show()
    
    
def inspect_words_over_time(df_with_topics, topic_to_evaluate, list_words, resampling, smoothing, max_value_y):

    df_with_topics_selected_topic = df_with_topics.loc[df_with_topics[topic_to_evaluate] == 1] 
    df_with_topics_selected_topic = df_with_topics_selected_topic.set_index('date')  
    
    df_with_topics_freq = df_with_topics_selected_topic.resample(resampling).size().reset_index(name="count")
    df_with_topics_freq = df_with_topics_freq.set_index('date')
    
    for word in list_words:
        df_with_topics_selected_topic[word] = df_with_topics_selected_topic["text"].str.contains(pat = word).astype(int) #''' Check here '''
    df_with_topics_selected_topic = df_with_topics_selected_topic[list_words] 
    df_with_topics_selected_topic = df_with_topics_selected_topic.resample(resampling).sum()
    
    df_with_topics_selected_topic = df_with_topics_selected_topic.div(df_with_topics_freq["count"], axis=0)
    df_with_topics_selected_topic = df_with_topics_selected_topic.fillna(0)
        
    x = pd.Series(df_with_topics_selected_topic.index.values)
    x = x.dt.to_pydatetime().tolist()
    
    df_with_topics_selected_topic = df_with_topics_selected_topic * 100

    sigma = (np.log(len(x)) - 1.25) * 1.2 * smoothing

    fig, ax1 = plt.subplots()
    for word in df_with_topics_selected_topic:
        ysmoothed = gaussian_filter1d(df_with_topics_selected_topic[word].tolist(), sigma=sigma)
        ax1.plot(x, ysmoothed, label=word, linewidth=2)
    
    ax1.set_xlabel('Time', fontsize=12, fontweight="bold")
    ax1.set_ylabel('Word appearance in documents related to the topic \n over time (% of documents)', fontsize=12, fontweight="bold")
    ax1.legend(prop={'size': 10})
    
    ax1.set_ylim([0,max_value_y])
    
    fig.tight_layout() 
    plt.figure(figsize=(20,14), dpi= 400)

    plt.rcParams["figure.figsize"] = [12,6]
    plt.show()

def inspect_words_over_time_based_on_most_frequent_words(df_with_topics, dict_anchor_words, model_and_vectorized_data, topic_to_evaluate, number_of_words, resampling, smoothing, max_value_y):
    topic_to_evaluate_number = topic_int_or_string(topic_to_evaluate, dict_anchor_words)
    list_words = list(list(zip(*model_and_vectorized_data[0].get_topics(topic=topic_to_evaluate_number, n_words=number_of_words)))[0])
    inspect_words_over_time(df_with_topics, topic_to_evaluate_number, list_words, resampling, smoothing, max_value_y)

def inspect_words_over_time_based_on_own_list(df_with_topics, dict_anchor_words, topic_to_evaluate, list_words, resampling, smoothing, max_value_y):
    topic_to_evaluate_number = topic_int_or_string(topic_to_evaluate, dict_anchor_words)
    inspect_words_over_time(df_with_topics, topic_to_evaluate_number, list_words, resampling, smoothing, max_value_y)




