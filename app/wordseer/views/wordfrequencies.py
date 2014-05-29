"""Word frequencies and bar charts
"""

from flask import request
from flask import abort
from flask.json import jsonify
from flask.views import View
from sqlalchemy.sql import func

from app import app
from app import db
from .. import wordseer
from .. import utils
from ...uploader.models import Word
from ...uploader.models import word_in_sentence

PAGE_SIZE = 100

class WordFrequencies(View):
    def dispatch_request(self):
        """Dispatch the request to this page.
        """

        words = request.args.get("words")
        page = request.args.get("page")

        if page:
            results = self.get_word_frequencies(words.replace("*", "%"), page)
            return jsonify(results)

        else:
            abort(400)

    def get_word_frequencies(self, words, page):
        """Get the frequencies of the given words, returning the given page
        of the pagination.

        Arguments:
            words (string): A string of comma separated words (TODO: why not
                make this a list?
            page (int): This function automatically paginates the result
                of the database query. Each page contains ``PAGE_SIZE`` number
                of entries, a config variable set at the top of this file.

        Retruns:
            list: A list in which every item is a dict which holds the id,
                word, pos, and length of the sentences attributes of every
                word retrieved from the database.
        """
        answer = []
        offset = page * PAGE_SIZE

        if words:
            wordlist = words.split(",")
            for word in wordlist:
                result = db.session.query(Word,
                    func.count(word_in_sentence.c.word_id).label("sentences")
                ).join(word_in_sentence).\
                    group_by(Word).\
                    order_by("sentences").\
                    limit(PAGE_SIZE).\
                    offset(offset).\
                    filter(Word.word.like(word)).\
                    all()

                for word in result:
                    answer.append({
                        "id": word.id,
                        "word": word.word,
                        "pos": word.pos,
                        "sentence_count": len(word.sentences),
                    })
        else:
            result = db.session.query(Word,
                func.count(word_in_sentence.c.word_id).label("sentences")
            ).join(word_in_sentence).\
                group_by(Word).\
                order_by("sentences").\
                limit(PAGE_SIZE).\
                offset(offset).\
                all()

            for word in result:
                answer.append({
                    "id": word.id,
                    "word": word.word,
                    "pos": word.pos,
                    "sentence_count": word.sentence_count,
                })

        return answer

wordseer.add_url_rule('/word-frequencies/get-frequent-words',
    view_func=WordFrequencies.as_view("word_frequencies"))

