/*
Copyright (c) 2003-2011, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/


CKEDITOR.editorConfig = function( config )
{
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';
    config.height = '500px';
    config.filebrowserUploadUrl = '/ckeditor/upload/'
    config.filebrowserBrowseUrl= '/ckeditor/browse/'
    config.skin = 'kama'

    config.toolbar = 'Palantir';

    config.toolbar_Palantir =
    [
        { name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','Scayt' ] },
        { name: 'styles', items : [ 'Styles','Format' ] },
        { name: 'basicstyles', items : [ 'Bold','Italic','Strike','-','RemoveFormat' ] },
        { name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote', 
        '-','JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock' ]},
        { name: 'insert', items : [ 'HorizontalRule','SpecialChar' ] },
    ];

};


