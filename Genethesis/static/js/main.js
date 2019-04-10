if (document.getElementById('customCheckRegister')) {
    document.getElementById('customCheckRegister').addEventListener('change', function(){
    
        register = document.getElementById('register');
    
        if (register.type == 'button') {
            register.classList.remove('disabled');
            register.type = 'submit';
        } else {
            register.classList.add('disabled');
            register.type = 'button';
        };
    
    });
}


if (document.getElementById('toggle-edit-info')) {

    document.getElementById('toggle-edit-info').addEventListener('click', function(){

        if (this.classList.contains('editing')) {
            oldInfoFields = document.getElementsByClassName('old-info');
            for (i=0; i<oldInfoFields.length; i++) {
                oldInfoFields[i].classList.remove('hidden');
                oldInfoFields[i].nextElementSibling.classList.add('hidden');
            };
            this.innerHTML = '编辑信息';
            document.getElementById('submit-edit-info').classList.add('hidden');
            this.classList.remove('editing');
        } else {
            oldInfoFields = document.getElementsByClassName('old-info');
            for (i=0; i<oldInfoFields.length; i++) {
                oldInfoFields[i].classList.add('hidden');
                oldInfoFields[i].nextElementSibling.classList.remove('hidden');
            };
            this.innerHTML = '取消编辑';
            document.getElementById('submit-edit-info').classList.remove('hidden');
            this.classList.add('editing');
        }


    });
}

if (document.getElementsByClassName('grid').length > 0) {
    var qsRegex;

    var $container = $('.grid').isotope({
        // options
        itemSelector: '.grid-item',
        layoutMode: 'masonry',
        filter: function() {
            return qsRegex ? $(this).attr('data-filename').match( qsRegex ) : true;
        }
    });
    var initShow = 12; //number of items loaded on init & onclick load more button
    var counter = initShow; //counter for load more button
    var iso = $container.data('isotope'); // get Isotope instance
    var $filterCount = $('#counter-number');
    // use value of search field to filter
    var $quicksearch = $('#search-field').keyup( debounce( function() {
        qsRegex = new RegExp( $quicksearch.val(), 'gi' );
        $container.isotope();
        loadMore(initShow);
        $('#counter-text').text('搜索结果');
        updateFilterCount();

        if (!$quicksearch.val()) {
            $('#counter-text').text('我的所有插图');
        };
    }, 200 ) );

    function updateFilterCount() {
        $filterCount.text( iso.filteredItems.length );
      }

    loadMore(initShow)

    //execute function onload
    $(window).on("load", function() {
        loadMore(initShow)
    });

    function loadMore(toShow) {
        $container.find(".hidden").removeClass("hidden");
    
        var hiddenElems = iso.filteredItems.slice(toShow, iso.filteredItems.length).map(function(item) {
            return item.element;
        });
        $(hiddenElems).addClass('hidden');
        $container.isotope('layout');
    
        //when no more to load, hide show more button
        if (hiddenElems.length == 0) {
            jQuery("#btn-load-more").html('没有更多了～');
        } else {
            jQuery("#btn-load-more").html('加载更多');
        };
    }

    //when load more button clicked
    $("#btn-load-more").click(function() {
        counter = counter + initShow;
        loadMore(counter);
    });

    // debounce so filtering doesn't happen every millisecond
    function debounce( fn, threshold ) {
        var timeout;
        threshold = threshold || 100;
        return function debounced() {
        clearTimeout( timeout );
        var args = arguments;
        var _this = this;
        function delayed() {
            fn.apply( _this, args );
        }
        timeout = setTimeout( delayed, threshold );
        };
    }

    /* Delete Illustrations */
    deleteButtons = document.getElementsByClassName("illustration-delete");
    for (i=0; i<deleteButtons.length; i++) {
        deleteButtons[i].addEventListener("click", function(){
            var c = confirm("确定删除该插图吗？该操作不可撤销。")
            if (c==true) {
                $.ajax({
                    type: "POST",
                    url: '/illustrations/delete/' + this.dataset.filename,
                    success: function(){
                        window.location.reload();
                    }
                });
            }
        });
    }
}

if (document.getElementsByClassName('clipboard-trigger').length > 0) {
    new ClipboardJS('.clipboard-trigger');
}

if (document.getElementsByClassName('tree').length > 0) {

    (function($) {
        $.fn.inputFilter = function(inputFilter) {
        return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function() {
            if (inputFilter(this.value)) {
            this.oldValue = this.value;
            this.oldSelectionStart = this.selectionStart;
            this.oldSelectionEnd = this.selectionEnd;
            } else if (this.hasOwnProperty("oldValue")) {
            this.value = this.oldValue;
            this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
            }
        });
        };
    }(jQuery));
    $('#chapter-total-number').inputFilter(function(value) {
        return /^\d*$/.test(value);
    });
    $('#chapter-total-number').on('keyup', function() {
        chapterNumberToBe = $(this).val();
        chapterNumberNow = $(this).siblings('.chapter').length;
        chaptersToChange = chapterNumberToBe - chapterNumberNow;
        if (chaptersToChange > 0) {
            for (chapterNumber=chapterNumberNow+1;chapterNumber<=chapterNumberToBe;chapterNumber++) {
                $(this).parent().append('<div class="chapter"><span class="chapter-number">' + chapterNumber +'</span><input type="text" class="chapter-title-input input-field" placeholder="章节标题" data-indent=0><div class="actions"><a href="#!" class="ml-5"><i class="fas fa-plus add-subchapter"></i></a><a href="#!" class="ml-2"><i class="fas fa-minus remove-subchapter"></i></a></div></div>')
            }
        } else {
            for (chapterNumber=chapterNumberNow;chapterNumber>chapterNumberToBe;chapterNumber--) {
                $(this).siblings('.chapter').last().remove();
            }
        }
    });

    $(document).on('click', '.add-subchapter', function() {
        chapterNumber = $(this).parent().parent().siblings('.chapter-number').text();
        subchapterNumber = $(this).parent().parent().siblings('.subchapter').length + 1;
        if ($(this).parent().parent().siblings('.subchapter').length > 0) {
            $(this).parent().parent().siblings('.subchapter').last().after('<div class="subchapter ml-5"><span class="subchapter-number">' + chapterNumber + '.' + subchapterNumber + '</span><input type="text" class="subchapter-title-input input-field" placeholder="子章节标题" data-indent=1><div class="actions"><a href="#!" class="ml-5"><i class="fas fa-plus add-scsubchapter"></i></a><a href="#!" class="ml-2"><i class="fas fa-minus remove-scsubchapter"></i></a></div></div>')
        } else {
            $(this).parent().parent().siblings('.chapter-title-input').after('<div class="subchapter ml-5"><span class="subchapter-number">' + chapterNumber + '.' + subchapterNumber + '</span><input type="text" class="subchapter-title-input input-field" placeholder="子章节标题" data-indent=1><div class="actions"><a href="#!" class="ml-5"><i class="fas fa-plus add-scsubchapter"></i></a><a href="#!" class="ml-2"><i class="fas fa-minus remove-scsubchapter"></i></a></div></div>')
        }
    })


    $(document).on('click', '.add-scsubchapter', function() {
        chapterNumber = $(this).parent().parent().siblings('.subchapter-number').text().split('.')[0];
        subchapterNumber = $(this).parent().parent().siblings('.subchapter-number').text().split('.')[1];
        scsubchapterNumber = $(this).parent().parent().siblings('.scsubchapter').length + 1;
        if ($(this).parent().parent().siblings('.scsubchapter').length > 0) {
            $(this).parent().parent().siblings('.scsubchapter').last().after('<div class="scsubchapter ml-5"><span class="scsubchapter-number">' + chapterNumber + '.' + subchapterNumber + '.' + scsubchapterNumber + '</span><input type="text" class="scsubchapter-title-input input-field" placeholder="次级子章节标题" data-indent=2></div>')
        } else {
            $(this).parent().parent().siblings('.subchapter-title-input').after('<div class="scsubchapter ml-5"><span class="scsubchapter-number">' + chapterNumber + '.' + subchapterNumber + '.' + scsubchapterNumber + '</span><input type="text" class="scsubchapter-title-input input-field" placeholder="次级子章节标题" data-indent=2></div>')
        }
    })

    $(document).on('click', '.remove-subchapter', function() {
        $(this).parent().parent().siblings('.subchapter').last().remove();
    });

    $(document).on('click', '.remove-scsubchapter', function() {
        $(this).parent().parent().siblings('.scsubchapter').last().remove();
    });

    $('.confirm-index').on('click', function() {
        $('.loader-overlay').removeClass('hidden');
        articleID = $('#articleID').text();
        article = {"id":articleID, chapters:[]}
        $('.chapter-title-input').each(function(){
            chapterTitle = $(this).val();
            chapterNumber = $(this).siblings('.chapter-number').first().text();
            article.chapters.push({"chapterNumber":chapterNumber, "title":chapterTitle, subChapters:[]})
            $(this).siblings('.subchapter').each(function(){
                subChapterTitle = $(this).find('.subchapter-title-input').val();
                chapterNumber = $(this).find('.subchapter-number').text().split(/\.(?=[^\.]+$)/)[0];
                subChapterNumber = $(this).find('.subchapter-number').text().split(/\.(?=[^\.]+$)/)[1];
                chapter = article.chapters[chapterNumber-1]
                chapter.subChapters.push({"chapterNumber":chapterNumber, "subChapterNumber":subChapterNumber, "title":subChapterTitle, scSubChapters:[]})
                $(this).children('.scsubchapter').each(function(){
                    scSubChapterTitle = $(this).find('.scsubchapter-title-input').val();
                    chapterNumber = $(this).find('.scsubchapter-number').text().split('.')[0];
                    subChapterNumber = $(this).find('.scsubchapter-number').text().split('.')[1];
                    scSubChapterNumber = $(this).find('.scsubchapter-number').text().split('.')[2];
                    subchapter = article.chapters[chapterNumber-1].subChapters[subChapterNumber-1]
                    subchapter.scSubChapters.push({"chapterNumber":chapterNumber, "subChapterNumber":subChapterNumber, "scSubChapterNumber":scSubChapterNumber, "title":scSubChapterTitle})
                });
            });
        });
        $.ajax({
            type: "POST",
            url: '/articles/inicialize/'+String(article.id),
            data: JSON.stringify(article),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: () => {
                window.location.href = '/articles/'+String(article.id)
            }
        });
    });

};

if (document.getElementsByClassName('copy-image').length > 0) {

    new ClipboardJS('.copy-image',{ container: document.getElementById('imageModal') });
    $('.copy-image').on('click', function(){
        console.log('1')
        if ($('#image-comment').val()) {
            code = '{{ImageAnchor:'+$('#image-link').val()+', ImageComment:'+$('#image-comment').val()+'}}';
        } else {
            code = '{{ImageAnchor:'+$('#image-link').val()+'}}';
        }
        $(this).attr('data-clipboard-text', code);
        $(this).removeClass('btn-primary');
        $(this).addClass('btn-success');
        $(this).text('复制成功')
    })
    $('#imageModal').on('show.bs.modal', function (e) {
        $('.copy-image').removeClass('btn-success');
        $('.copy-image').addClass('btn-primary');
        $('.copy-image').text('复制代码');
    })
}

if (document.getElementById('add-entry')) {

    $("input[name='referenceKind']").on('change', function(){
        type = $("input[name='referenceKind']:checked").val();
        language = $("input[name='language']:checked").val();
        $('.input-master').children().addClass('hidden');
        $('.input-master').children().children().addClass('hidden');
        $('.'+language).removeClass('hidden');
        $('.'+type).removeClass('hidden');
    })

    $("input[name='language']").on('change', function(){
        type = $("input[name='referenceKind']:checked").val();
        language = $("input[name='language']:checked").val();
        $('.input-master').children().addClass('hidden');
        $('.input-master').children().children().addClass('hidden');
        $('.'+language).removeClass('hidden');
        $('.'+type).removeClass('hidden');
    })


    $('#add-entry').on('click', function(){
        language = $("input[name='language']:checked").val();
        type = $("input[name='referenceKind']:checked").val();
        console.log(type, language)
        inputMaster = $('.'+language).children('.'+type);
        text = '';
        if (language=='zh'){
            if (type=='book') {
                text = inputMaster.find('.input-author').val() + '：';
                text = text + '《' + inputMaster.find('.input-title').val() + '》';
                if (inputMaster.find('.input-translator').val()) {
                    text = text + '（' + inputMaster.find('.input-translator').val() + '译）'
                };
                text = text + '，' + inputMaster.find('.input-city').val() + '：';
                text = text + inputMaster.find('.input-publisher').val() + '，';
                text = text + inputMaster.find('.input-year').val() + '年;';
            }
            if (type=='mag') {
                text = inputMaster.find('.input-author').val() + '：';
                text = text + '“' + inputMaster.find('.input-title').val() + '”';
                text = text + '，原载于《' + inputMaster.find('.input-magname').val() + '》';
                text = text + '，' + inputMaster.find('.input-year').val() + '年第' + inputMaster.find('.input-num').val() + '期';
                text = text + '，第' + inputMaster.find('.input-page').val() + '页';
                text = text + '，' + inputMaster.find('.input-city').val() + '：';
                text = text + inputMaster.find('.input-publisher').val() + ';';
            }
            if (type=='comp') {
                text = inputMaster.find('.input-author').val() + '：';
                text = text + '“' + inputMaster.find('.input-title').val() + '”';
                text = text + '，见' + inputMaster.find('.input-compauthor').val() + '编';
                text = text + '《' + inputMaster.find('.input-compname').val() + '》';
                text = text + '，第' + inputMaster.find('.input-page').val() + '页';
                text = text + '，' + inputMaster.find('.input-city').val() + '：';
                text = text + inputMaster.find('.input-publisher').val();
                text = text + '，' + inputMaster.find('.input-year').val() + '年;';
            }
            if (type=='elec') {
                text = inputMaster.find('.input-website').val() + '：';
                text = text + '《' + inputMaster.find('.input-title').val() + '》';
                text = text + '，' + inputMaster.find('.input-link').val();
                text = text + '，' + inputMaster.find('.input-year').val() + '年;';
            }
        }
        if (language=='nzh'){
            if (type=='book') {
                text = inputMaster.find('.input-author-ln').val().toUpperCase() + ', ';
                text = text + inputMaster.find('.input-author-fn').val() + ': ';
                text = text + '"' + inputMaster.find('.input-title').val() + '"';
                text = text + ', ' + inputMaster.find('.input-city').val();
                text = text + ', ' + inputMaster.find('.input-publisher').val();
                text = text + ', ' + inputMaster.find('.input-year').val() + ';';
            }
            if (type=='mag') {
                text = inputMaster.find('.input-author-ln').val().toUpperCase() + ', ';
                text = text + inputMaster.find('.input-author-fn').val() + ': ';
                text = text + inputMaster.find('.input-title').val();
                text = text + ', ' + inputMaster.find('.input-magname').val();
                text = text + ', ' + inputMaster.find('.input-publisher').val();
                text = text + ', ' + inputMaster.find('.input-city').val();
                text = text + ', ' + inputMaster.find('.input-year').val();
                text = text + ', nº ' + inputMaster.find('.input-num').val();
                text = text + ', pp. ' + inputMaster.find('.input-page').val() + ';';
            }
            if (type=='comp') {
                text = inputMaster.find('.input-author-ln').val().toUpperCase() + ', ';
                text = text + inputMaster.find('.input-author-fn').val() + ': ';
                text = text + inputMaster.find('.input-title').val();
                text = text + ', en ' + inputMaster.find('.input-compauthor-ln').val().toUpperCase();
                text = text + ', ' + inputMaster.find('.input-compauthor-fn').val();
                text = text + ', ' + inputMaster.find('.input-compname').val();
                text = text + ', ' + inputMaster.find('.input-city').val();
                text = text + ', ' + inputMaster.find('.input-publisher').val();
                text = text + ', ' + inputMaster.find('.input-year').val();
                text = text + ', pp. ' + inputMaster.find('.input-page').val() + ';';
            }
            if (type=='elec') {
                text = inputMaster.find('.input-website').val() + ': ';
                text = text + '"' + inputMaster.find('.input-title').val() + '"';
                text = text + ', ' + inputMaster.find('.input-link').val();
                text = text + ', ' + inputMaster.find('.input-year').val() + ';';
            }
        }
        if ($('#input-content').val()) {
            $('#input-content').append('\n'+text);
        } else {
            $('#input-content').append(text);
        }
    });
}

if (document.getElementById('pro-mode-toggle')) {
    $('#pro-mode-toggle').on('change', function(){
        $('#pro-mode').toggleClass('no-display');
    })
}

if (document.getElementById('input-language')) {
    $('#input-language').on('change', function(){
        language = $(this).val();
        if (language == 'zh') {
            $('#input-marginTop').val(2.0)
            $('#input-marginBottom').val(2.5)
            $('#input-marginLeft').val(3.0)
            $('#input-marginRight').val(2.5)
            $('#input-sectionTitleFont').val('ht')
            $('#input-sectionTitleFontAlt').val('tnr')
            $('#input-titleFont').val('st')
    
            $('#input-bodyFont').val('st')
            $('#input-abstractFont').val('st')
            $('#input-abstractFontAlt').val('tnr')
            $('#input-imageCommentFont').val('ht')
            $('#input-noteFont').val('st')
            $('#input-bibliographyFont').val('st')
            $('#input-bibliographyFontAlt').val('tnr')
            $('#input-tocFont').val('st')
            $('#input-innerCoverFont').val('st')
            $('#input-innerCoverFontAlt').val('tnr')
    
            $('#input-sectionTitleFontSize').val(16)
            $('#input-title1FontSize').val(12)
            $('#input-title2FontSize').val(12)
            $('#input-title3FontSize').val(12)
            $('#input-bodyFontSize').val(12)
            $('#input-abstractFontSize').val(12)
            $('#input-imageCommentFontSize').val(12)
            $('#input-noteFontSize').val(9)
            $('#input-bibliographyFontSize').val(10.5)
            $('#input-toc1FontSize').val(12)
            $('#input-toc2FontSize').val(12)
            $('#input-toc3FontSize').val(12)
            $('#input-innerCoverFontSize').val(22)
    
            $('#input-sectionTitleLineSpacing').val(2.00)
            $('#input-title1LineSpacing').val(1.50)
            $('#input-title2LineSpacing').val(1.50)
            $('#input-title3LineSpacing').val(1.50)
            $('#input-tocLineSpacing').val(1.50)
            $('#input-bodyLineSpacing').val(1.50)
            $('#input-abstractLineSpacing').val(1.50)
            $('#input-bibliographyLineSpacing').val(1.00)
            $('#input-innerCoverLineSpacing').val(1.50)
    
            $('#input-title1AfterSpacing').val(0.00)
            $('#input-title2AfterSpacing').val(0.00)
            $('#input-title3AfterSpacing').val(0.00)
            $('#input-bodyAfterSpacing').val(0.00)
            $('#input-abstractAfterSpacing').val(0.00)
            $('#input-bibliographyAfterSpacing').val(1.00)
            $('#input-toc1BeforeSpacing').val(0.75)
            $('#input-toc2BeforeSpacing').val(0.00)
    
            $('#input-title1Indent').val(0)
            $('#input-title2Indent').val(0)
            $('#input-title3Indent').val(0)
            $('#input-toc1Indent').val(0)
            $('#input-toc2Indent').val(2)
            $('#input-toc3Indent').val(4)
            $('#input-bodyFirstIndent').val(2)
            $('#input-abstractFirstIndent').val(2)
            $('#input-bodyLeftIndent').val(0)
            $('#input-abstractLeftIndent').val(0)
        };
        if (language == 'es') {
            $('#input-marginTop').val(2.0)
            $('#input-marginBottom').val(2.5)
            $('#input-marginLeft').val(3.0)
            $('#input-marginRight').val(2.5)

            $('#input-sectionTitleFont').val('tnr')
            $('#input-sectionTitleFontAlt').val('ht')
            $('#input-titleFont').val('tnr')
            $('#input-bodyFont').val('tnr')
            $('#input-abstractFont').val('tnr')
            $('#input-abstractFontAlt').val('st')
            $('#input-imageCommentFont').val('tnr')
            $('#input-noteFont').val('tnr')
            $('#input-bibliographyFont').val('tnr')
            $('#input-bibliographyFontAlt').val('st')
            $('#input-tocFont').val('tnr')
            $('#input-innerCoverFont').val('tnr')
            $('#input-innerCoverFontAlt').val('st')
    
            $('#input-sectionTitleFontSize').val(16)
            $('#input-title1FontSize').val(12)
            $('#input-title2FontSize').val(12)
            $('#input-title3FontSize').val(12)
            $('#input-bodyFontSize').val(12)
            $('#input-abstractFontSize').val(12)
            $('#input-imageCommentFontSize').val(12)
            $('#input-noteFontSize').val(9)
            $('#input-bibliographyFontSize').val(10.5)
            $('#input-toc1FontSize').val(12)
            $('#input-toc2FontSize').val(12)
            $('#input-toc3FontSize').val(12)
            $('#input-innerCoverFontSize').val(22)
    
            $('#input-sectionTitleLineSpacing').val(2.00)
            $('#input-title1LineSpacing').val(1.50)
            $('#input-title2LineSpacing').val(1.50)
            $('#input-title3LineSpacing').val(1.50)
            $('#input-tocLineSpacing').val(1.50)
            $('#input-bodyLineSpacing').val(1.50)
            $('#input-abstractLineSpacing').val(1.50)
            $('#input-bibliographyLineSpacing').val(1.00)
            $('#input-innerCoverLineSpacing').val(1.50)
    
            $('#input-title1AfterSpacing').val(0.00)
            $('#input-title2AfterSpacing').val(0.00)
            $('#input-title3AfterSpacing').val(0.00)
            $('#input-bodyAfterSpacing').val(0.00)
            $('#input-abstractAfterSpacing').val(0.00)
            $('#input-bibliographyAfterSpacing').val(1.00)
            $('#input-toc1BeforeSpacing').val(0.75)
            $('#input-toc2BeforeSpacing').val(0.00)
    
            $('#input-title1Indent').val(0)
            $('#input-title2Indent').val(0)
            $('#input-title3Indent').val(0)
            $('#input-toc1Indent').val(0)
            $('#input-toc2Indent').val(2)
            $('#input-toc3Indent').val(4)
            $('#input-bodyFirstIndent').val(2)
            $('#input-abstractFirstIndent').val(2)
            $('#input-bodyLeftIndent').val(0)
            $('#input-abstractLeftIndent').val(0)
        };
    });
}

if(document.getElementsByClassName('preview').length > 0) {
    $('.articles-action.preview').on('click', function(){

        articleID = String($(this).attr('data-id'));

        $('.loader-overlay').removeClass('hidden')

        $.ajax({
            type: "POST",
            url: '/articles/' + articleID + '/download',
            success: function(){
                $('.loader-overlay').addClass('hidden');
                $('#downloader').attr('src', '/articles/' + articleID + '/download');
                $.notify({
                    // options
                    message: '您的论文已经准备好，如果下载没有自动开始，请换个浏览器，比如Chrome或者Safari，真的不要用野鸡浏览器了，程序猿求你了。',
                    },{
                    // settings
                    placement: {
                        from: "top",
                        align: "right",
                    },
                    type: 'success',
                    offset: {
                        x: 20,
                        y: 20,
                    },
                });
            }
        });

    })
}

var toolbarOptions = [
    ['bold', 'italic', 'underline'],
    ['image', 'link']
]
var icons = Quill.import('ui/icons');
icons['link'] = '<i class="far fa-sticky-note quill-toolbar-icon"></i>';

$('.og-content').each(function(i){
    content = $(this).text()

    quill = new Quill('#editor-'+String(i+1), {
        modules: {
            toolbar: toolbarOptions
        },
        placeholder: '开始撰写内容...',
        theme: 'snow'
    });
    var Delta = Quill.import('delta');
    quill.clipboard.addMatcher (Node.ELEMENT_NODE, function (node, delta) {
        var plaintext = $ (node).text ();
        return new Delta().insert (plaintext);
    });
    imageUI = function() {
        $('#imageModal').modal('show');
    }
    var toolbar = quill.getModule('toolbar');
    toolbar.addHandler('image', imageUI);
    if (content!='') {
        text = content;
        while (text != '') {
            if (text.search('{{') != -1) {
                runText = text.slice(0, text.search('{{'));
            } else {
                runText = text;
            }
            // If the next spAttr is footnote, render the reference point here.
            options = {
                'bold': false,
                'italic': false,
                'underline': false,
                'link': false
            }
            quill.insertText(quill.getLength()-1, runText, options);
            // If there is a special run
            if (text.search('{{') != -1) {
                spOg = text.slice(text.search('{{'), text.search('}}')+2);
                spRun = text.slice(text.search('{{')+2, text.search('}}'));
                spAttrs = spRun.slice(0, spRun.search(':')).split('&');
                spText = spRun.slice(spRun.search(':')+1);
                for (i=0;i<spAttrs.length;i++) {
                    spAttr = spAttrs[i]
                    options[spAttr] = true
                }
                if (spAttrs.includes('footnoteAnchor')) {
                    spLink = spText.slice(spText.search('footnoteContent:')+16)
                    spText = spText.slice(0, spText.search(', footnoteContent:'))
                    quill.insertText(quill.getLength()-1, spText, {'link':spLink});
                }
                if (spAttrs.includes('ImageAnchor')) {
                    quill.insertText(quill.getLength()-1, spOg, options);
                }
                if (!spAttrs.includes('ImageAnchor') && !spAttrs.includes('footnoteAnchor')) {
                    quill.insertText(quill.getLength()-1, spText, options);
                }
            }
            // Slice the rest
            if (text.search('}}') != -1){
                text = text.slice(text.search('}}')+2);
            } else {
                text = '';
            }
        }
        quill.deleteText(quill.getLength()-1, 1);
    }

})

$('.confirm').on('click', function(e){
    e.preventDefault();
    $('.og-content').each(function(i){
        quill = Quill.find(document.querySelector("#editor-"+String(i+1)))
        raw = quill.container.firstChild.innerHTML;
        raw = raw.replace(/<a href="([^"]+)" target="_blank">([^<]+)<\/a>/g, "{{footnoteAnchor:$2, footnoteContent:$1}}");
        raw = raw.replace(/<p>/g,'')
        raw = raw.replace(/<.p>/g,'\n')
        raw = raw.replace(/<br>\n/g,'')
        raw = raw.replace(/<strong><em><u>/g, '{{bold&italic&underline:')
        raw = raw.replace(/<.u><.em><.strong>/g, '}}')
        raw = raw.replace(/<strong><em>/g, '{{bold&italic:')
        raw = raw.replace(/<.em><.strong>/g, '}}')
        raw = raw.replace(/<strong><u>/g, '{{bold&underline:')
        raw = raw.replace(/<.u><.strong>/g, '}}')
        raw = raw.replace(/<em><u>/g, '{{italic&underline:')
        raw = raw.replace(/<.u><.em>/g, '}}')
        raw = raw.replace(/<strong>/g, '{{bold:')
        raw = raw.replace(/<.strong>/g, '}}')
        raw = raw.replace(/<em>/g, '{{italic:')
        raw = raw.replace(/<.em>/g, '}}')
        raw = raw.replace(/<u>/g, '{{underline:')
        raw = raw.replace(/<.u>/g, '}}')
        raw = raw.replace(/&nbsp;/g, '')
        raw = raw.replace(/&amp;nbsp;/g, '')
        raw = raw.replace(/&amp;amp;nbsp;/g, '')
        $(this).val(raw)
    })
    $('.content-form')[0].submit()
})

if (document.getElementsByClassName('masterCard')) {
    cards = $(".cardContainer");

    function transitionIn() {
        $(this).find('.flippingCard').addClass("activeCard");
    }
    function transitionOut() {
        $(this).find('.flippingCard').removeClass("activeCard");
    }

    cards.each(function(){
        $(this).on("mouseenter", transitionIn);
        $(this).on("mouseout", transitionOut);
    })

    $('.direct-link').each(function(){
        $(this).on('click', function(){
            window.location.href = $(this).attr('data-link')
        })
    })


    $('.cardContainer').filter(function () {
        return $(this).attr("data-chapter");
    }).each(function () {
        $(this).on('click', function () {
            $("html, body").animate({ scrollTop: 0 }, "slow");
            chapterNumber = $(this).attr("data-chapter")
            chapterCards = $('.chapter-'+chapterNumber)
            $('.cardModal').addClass('shown')
            chapterCards.addClass('shown')
            $('.cardModal .cardContainer:not(.shown)').addClass('no-display')
        })
    })

    $('.cardModal-overlay').on('click', function(){
        chapterCards = $('.chapter-'+chapterNumber)
        $('.cardModal').removeClass('shown')
        chapterCards.removeClass('shown')
        chapterCards.addClass('no-display')
        $('.cardModal').removeClass('shown')
        $('.cardModal .cardContainer').removeClass('no-display')
    })

}

if ($('.articles-action.finalize').length > 0) {
    $('.articles-action.finalize').on('click', function(){
        $('.loader-overlay').removeClass('hidden');
    })
}

if ($('.articles-action.delete').length > 0) {
    $('.articles-action.delete').on('click', function(){
        var c = confirm('是否确定删除该论文？该操作不可撤销。')
        if (c == true) {
            window.location.href = '/articles/'+String($(this).attr('data-id'))+'/delete'
        }
    })
}
