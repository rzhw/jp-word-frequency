#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2020 Richard Wang <https://github.com/rzhw>. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Fetch a Twitter list, use it to generate frequency of Japanese vocabulary
"""

from collections import OrderedDict
import json
import sys

import nagisa
import regex
import twitter
from t import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET, LIST_ID


def get_timeline(max_id=None):
    if max_id:
        return api.GetListTimeline(list_id=LIST_ID, max_id=max_id, count=200)
    return api.GetListTimeline(list_id=LIST_ID, count=200)


def get_tweets(api=None, screen_name=None):
    timeline = []
    earliest_tweet = None
    for i in range(20):
        tweets = get_timeline(earliest_tweet)
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


def validate_japanese(word):
    return (not regex.match(r'^\s*$', word) and not regex.match(r'\W', word)
            and regex.match(r'\p{Hiragana}|\p{Katakana}|\p{Han}', word))


if __name__ == "__main__":
    api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY,
                      ACCESS_TOKEN_SECRET)
    screen_name = sys.argv[1]
    print(screen_name)
    timeline = get_tweets(api=api, screen_name=screen_name)

    all_together = ''
    for tweet in timeline:
        all_together += tweet.text + "\n"

    print("hello")
    taggings = nagisa.filter(all_together,
                             filter_postags=[
                                 '補助記号', '空白', '助詞', '助動詞', '記号', 'URL', '英単語',
                                 'ローマ字文'
                             ])

    freq = {}
    for word in filter(validate_japanese, taggings.words):
        freq[word] = freq.get(word, 0) + 1

    # Sort by value
    sorted_freq = OrderedDict(sorted(freq.items(), key=lambda x: x[1]),
                              reverse=True)

    output = "Word,Count\n"
    for key, value in sorted_freq.items():
        output += "%s,%d\n" % (key, value)

    with open('output.csv', 'w+') as f:
        f.write(output)
