/* Copyright 2012 Aditi Muralidharan. See the file "LICENSE" for the full license governing this code. */
/** The skeleton for the Word Frequency graph views.
*/
Ext.define('WordSeer.view.visualize.wordfrequencies.WordFrequencies', {
	extend:'Ext.panel.Panel',
	layout: 'fit',
	alias:'widget.word-frequencies',
	autoScroll: true,
	dockedItems: [{
		xtype: 'toolbar',
		dock: 'top',
		itemId: 'tbar',
		items: [
			{
				xtype: 'checkbox',
				fieldLabel: 'Stacked',
				labelAlign: 'right',
				name: 'stacked',
				itemId: 'stacked',
				labelWidth: 50,
			},
			{
				xtype: 'checkbox',
				labelAlign: 'right',
				fieldLabel: 'Normalized',
				name: 'normalized',
				itemId: 'normalized',
				labelWidth: 60,
			},
			{
				xtype: 'checkbox',
				labelAlign: 'right',
				fieldLabel: 'Labels',
				name: 'labels',
				itemId: 'labels',
				labelWidth: 45,
			},
			]
	}],

	items: [
		{
			xtype: 'component',
			itemId: 'canvas',
			autoScroll: 'true',
			style: {
				"padding-left": "10px"
			}
		}
	],

	/** @property {Array} charts The word frequency chart objects belonging to this
	view.
	*/
	charts: [],

	/**
	@property {Array} chart_divs The word frequency chart views belonging to this
	view.
	*/
	chart_divs: [],

	/** @property {Array} As list of lists of search results matching a search query.
	*/
	data: [],

	/** @property {String} [top_n="all"] How many string facet values to show.
	*/
	top_n: 'all',

	initComponent:function(){
		/**
		@event search Fired when the user issues a search query or when the tree
		is loaded for the first time.
		@param {WordSeer.model.FormValues} formValues a
		formValues object representing a search query.
		@param {WordSeer.view.visualize.wordfrequencies.WordFrequencies} this view.
		*/
		/**
		@event draw Fired when a request for data from the server
		returns successfully.
		@param {WordSeer.view.visualize.wordfrequencies.WordFrequencies} this view.
		@param {Object} data An object containing one list of sentence records
		for each search that was issued.
		*/

		/**
		@event draw Fired when a request for data from the server
		returns successfully.
		@param {WordSeer.view.visualize.wordfrequencies.WordFrequencies} this view.
		@param {Object} data An object containing one list of sentence records
		for each search that was issued.
		*/
		this.addEvents('search', 'change');
		this.callParent(arguments);
		this.down('checkbox[name=stacked]').setValue(true);
		this.down('checkbox[name=labels]').setValue(true);
	}
});
