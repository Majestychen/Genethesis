console.log('1');
$(this).siblings('.subchapter').each(function(){
    subChapterTitle = $(this).find('.subchapter-title-input').val();
    chapterNumber = $(this).find('.subchapter-number').text().split(/\.(?=[^\.]+$)/)[0];
    subChapterNumber = $(this).find('.subchapter-number').text().split(/\.(?=[^\.]+$)/)[1];
    $.ajax({
        type: "POST",
        url: '/articles/'+ articleID +'/chapters/' + chapterNumber + '/subchapters/new',
        data: JSON.stringify({ "subChapterTitle" : subChapterTitle, "subChapterNumber": subChapterNumber } ),
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(){
            $(this).children('.scsubchapter').each(function(){
                console.log('2');
                scSubChapterTitle = $(this).find('.scsubchapter-title-input').val();
                chapterNumber = $(this).find('.scsubchapter-number').text().split(/\.(?=[^\.]+$)/)[0];
                subChapterNumber = $(this).find('.scsubchapter-number').text().split(/\.(?=[^\.]+$)/)[1];
                scSubChapterNumber = $(this).find('.scsubchapter-number').text().split(/\.(?=[^\.]+$)/)[2];
                $.ajax({
                    type: "POST",
                    url: '/articles/'+ articleID +'/chapters/' + chapterNumber + '/subchapters/' + SubChapterNumber + '/scsubchapters/new',
                    data: JSON.stringify({ "scSubChapterTitle" : scSubChapterTitle, "scSubChapterNumber": scSubChapterNumber } ),
                    contentType: "application/json; charset=utf-8",
                    dataType: "json",
                    success: function(){}
                });
            });
        }
    });
});