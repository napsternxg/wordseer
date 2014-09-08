"""Sentence models.
"""
from sqlalchemy.ext.associationproxy import association_proxy

from app import db
from .base import Base
from .project import Project
from .association_objects import DependencyInSentence
from .association_objects import WordInSentence
from .counts import WordCount, DependencyCount

class Sentence(db.Model, Base):
    """A model representing a sentence.

    The sentence model is treated like "leaf" units. It has a link to its
    parent unit as well as the top-level document. Sentences contain words
    (the model), and also stores its own raw text, for use in search results.

    Attributes:
        unit (Unit): The ``Unit`` containing this sentence.
        document (Document): the ``Document`` (top-level unit) to which this
            sentence belongs to.
        text (str): The raw text of the sentence.
        dependencies (list of Dependencies): ``Dependency``\s present in this
            sentence. This relationship is described with
            ``DependencyInSentence``.
        properties (list of Propertys): ``Property``\s associated with this
            ``Sentence``.
        words (list of Words): ``Word``\s in this ``Sentence``.

    Relationships:
        belongs to: unit, document
        has many: words, dependencies
    """

    # Attributes

    unit_id = db.Column(db.Integer, db.ForeignKey("unit.id"))
    document_id = db.Column(db.Integer, db.ForeignKey("document.id"))
    bigram_id = db.Column(db.Integer, db.ForeignKey("bigram_offset.id"))
    text = db.Column(db.Text, index=True)
    length = db.Column(db.Integer)

    # Relationships

    words = association_proxy("sentence_words", "word",
        creator=lambda word: WordInSentence(word=word))

    dependencies = association_proxy("sentence_dependencies", "dependency",
        creator=lambda dependency: DependencyInSentence(dependency=dependency))

    document = db.relationship("Document", foreign_keys=[document_id],
        backref="all_sentences")

    properties = db.relationship("Property", backref="sentence")

    def __repr__(self):
        """Representation of the sentence, showing its text.

        NOTE: could be trucated to save print space
        """

        return "<Sentence: " + str(self.text) + ">"

    def add_word(self, word, position=None, space_before="",
        part_of_speech="", surface=None, project=None, force=True):
        """Add a word to the sentence by explicitly creating the association
        object.

        Arguments:
            word (Word): The ``Word`` that should be added to this ``Sentence``.

        Keyword Arguments:
            position (int): The position (0-indexed) of ``word`` in this
                ``Sentence``.
            space_before (str): The space before ``word``, if any.
            part_of_speech (str): The part of speech of ``word``.
            project (Project): The ``Project`` that scopes this relationship

        Returns:
            WordInSentence: The association object that associates this
                ``Sentence`` and ``word``.
        """

        # project argument assigned active_project if not present
        if project == None: project = Project.active_project

        word_in_sentence = WordInSentence(
            word=word,
            surface=surface,
            project=project,
            sentence=self,
            position=position,
            space_before=space_before,
            part_of_speech=part_of_speech,
        )

        word_in_sentence.save(force=force)

        return word_in_sentence

    def add_dependency(self, dependency, governor_index=None,
        dependent_index=None, project=None, force=True):
        """Add a dependency to the sentence by explicitly creating the
        association object.

        Arguments:
            dependency (Dependency): The ``Dependency`` in this relationship.

        Keyword Arguments:
            governor_index (int): Position (0-indexed) of the governor in this
                ``Sentence``. Default is ``None``.
            dependent_index (int): Position (0-indexed) of the dependent in this
                ``Sentence``. Default is ``None``.

        Returns:
            DependencyInSentence: The association object that associates this
                ``Sentence`` and ``dependency``.
        """

        # project argument assigned active_project if not present
        if project == None: project = Project.active_project

        dependency_in_sentence = DependencyInSentence(
            dependency=dependency,
            sentence=self,
            project=project,
            document=self.document,
            governor_index=governor_index,
            dependent_index=dependent_index
        )

        dependency_in_sentence.save(force=force)

        return dependency_in_sentence

