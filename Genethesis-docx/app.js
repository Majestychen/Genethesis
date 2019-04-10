const express = require('express');
const app = express();
const port = 3000;
const sqlite3 = require('sqlite3').verbose();
const _ = require('underscore');
const docx = require("docx");
const fs = require("fs");
const sizeOf = require('image-size');
const docxConverter = require('docx-pdf');
var { Document, Paragraph, Packer, Numbering, Indent, TableOfContents, StyleLevel, TextRun, TextWrappingType, TextWrappingSide, HorizontalPositionRelativeFrom, HorizontalPositionAlign, VerticalPositionRelativeFrom, VerticalPositionAlign, PageNumberFormat } = docx;
//import { Document, Indent, Numbering, Packer, Paragraph } from 'docx';

app.set('view engine', 'pug')

let db = new sqlite3.Database('../Genethesis/site.db', (err) => {
    if (err) {
      return console.error(err.message);
    }
    console.log('Connected to the SQlite database.');
});

app.get('/test/docx/:articleID', (req, res) => {
    let article_id = req.params.articleID;

    // Get article and organize data 

    let sql = `SELECT article.*, 
    chapter.title AS cT, chapter.chapterNumber AS cN, chapter.content AS cC, chapter.tailContent AS ctC,
    sub_chapter.title AS scT, sub_chapter.subChapterNumber AS scN, sub_chapter.content AS scC, sub_chapter.tailContent AS sctC,
    sc_sub_chapter.title AS sscT, sc_sub_chapter.scSubChapterNumber AS sscN, sc_sub_chapter.content AS sscC
    FROM article 
    LEFT JOIN chapter ON article.id = chapter.articleID
    LEFT JOIN sub_chapter ON chapter.id = sub_chapter.chapterID
    LEFT JOIN sc_sub_chapter ON sub_chapter.id = sc_sub_chapter.subChapterID
    WHERE article.id = ?
    ORDER BY
    	chapterNumber ASC,
        subChapterNumber ASC,
        scSubChapterNumber ASC`;
    db.all(sql, [article_id], (err, entries) => {
        if (err) {
            console.log(err)
        };
        var article = {
            "id": entries[0].id,
            "title": entries[0].title,
            "titleAlt": entries[0].titleAlt,
            "authorID": entries[0].userID,
            "language": entries[0].language,
            "tutor": entries[0].tutor,
            "abstract1": entries[0].abstract1,
            "abstract2Toggle": entries[0].abstract2Toggle,
            "abstract2": entries[0].abstract2,
            "introduction": entries[0].introduction,
            "keywords": entries[0].keywords,
            "keywordsAlt": entries[0].keywordsAlt,
            "bibliography": entries[0].bibliography,
            "gratitude": entries[0].gratitude,
            "marginTop": entries[0].marginTop,
            "marginLeft": entries[0].marginLeft,
            "marginBottom": entries[0].marginBottom,
            "marginRight": entries[0].marginRight,
            "sectionTitleFont": entries[0].sectionTitleFont,
            "sectionTitleFontAlt": entries[0].sectionTitleFontAlt,
            "titleFont": entries[0].titleFont,
            "bodyFont": entries[0].bodyFont,
            "abstractFont": entries[0].abstractFont,
            "abstractFontAlt": entries[0].abstractFontAlt,
            "imageCommentFont": entries[0].imageCommentFont,
            "noteFont": entries[0].noteFont,
            "bibliographyFont": entries[0].bibliographyFont,
            "bibliographyFontAlt": entries[0].bibliographyFontAlt,
            "tocFont": entries[0].tocFont,
            "innerCoverFont": entries[0].innerCoverFont,
            "innerCoverFontAlt": entries[0].innerCoverFontAlt,
            "sectionTitleFontSize": entries[0].sectionTitleFontSize,
            "title1FontSize": entries[0].title1FontSize,
            "title2FontSize": entries[0].title2FontSize,
            "title3FontSize": entries[0].title3FontSize,
            "bodyFontSize": entries[0].bodyFontSize,
            "abstractFontSize": entries[0].abstractFontSize,
            "imageCommentFontSize": entries[0].imageCommentFontSize,
            "noteFontSize": entries[0].noteFontSize,
            "bibliographyFontSize": entries[0].bibliographyFontSize,
            "toc1FontSize": entries[0].toc1FontSize,
            "toc2FontSize": entries[0].toc2FontSize,
            "toc3FontSize": entries[0].toc3FontSize,
            "innerCoverFontSize": entries[0].innerCoverFontSize,
            "sectionTitleLineSpacing": entries[0].sectionTitleLineSpacing,
            "title1LineSpacing": entries[0].title1LineSpacing,
            "title2LineSpacing": entries[0].title2LineSpacing,
            "title3LineSpacing": entries[0].title3LineSpacing,
            "tocLineSpacing": entries[0].tocLineSpacing,
            "bodyLineSpacing": entries[0].bodyLineSpacing,
            "abstractLineSpacing": entries[0].abstractLineSpacing,
            "imageCommentLineSpacing": entries[0].imageCommentLineSpacing,
            "noteLineSpacing": entries[0].noteLineSpacing,
            "bibliographyLineSpacing": entries[0].bibliographyLineSpacing,
            "innerCoverLineSpacing": entries[0].innerCoverLineSpacing,
            "title1AfterSpacing": entries[0].title1AfterSpacing,
            "title2AfterSpacing": entries[0].title2AfterSpacing,
            "title3AfterSpacing": entries[0].title3AfterSpacing,
            "bodyAfterSpacing": entries[0].bodyAfterSpacing,
            "abstractAfterSpacing": entries[0].abstractAfterSpacing,
            "bibliographyAfterSpacing": entries[0].bibliographyAfterSpacing,
            "toc1BeforeSpacing": entries[0].toc1BeforeSpacing,
            "toc2BeforeSpacing": entries[0].toc2BeforeSpacing,
            "title1Indent": entries[0].title1Indent,
            "title2Indent": entries[0].title2Indent,
            "title3Indent": entries[0].title3Indent,
            "toc1Indent": entries[0].toc1Indent,
            "toc2Indent": entries[0].toc2Indent,
            "toc3Indent": entries[0].toc3Indent,
            "bodyFirstIndent": entries[0].bodyFirstIndent,
            "abstractFirstIndent": entries[0].abstractFirstIndent,
            "bodyLeftIndent": entries[0].bodyLeftIndent,
            "abstractLeftIndent": entries[0].abstractLeftIndent,
            "chapters":[]
        };
        for (i in entries) {
            if (_.findWhere(article.chapters, {"chapterNumber":entries[i].cN}) == null) {
                article.chapters.push({"chapterNumber":entries[i].cN, "title":entries[i].cT, "content":entries[i].cC, "tailContent":entries[i].ctC, "subChapters":[]})
            }
        };
        for (i in entries) {
            if (entries[i].scN){
                chapter = _.findWhere(article.chapters, {"chapterNumber":entries[i].cN})
                if (_.findWhere(chapter.subChapters, {"subChapterNumber":entries[i].scN}) == null) {
                    chapter.subChapters.push({"chapterNumber":entries[i].cN, "subChapterNumber":entries[i].scN, "title":entries[i].scT, "content":entries[i].scC, "tailContent":entries[i].sctC, "scSubChapters":[]})
                }
            }
        };
        for (i in entries) {
            if (entries[i].sscN){
                chapter = _.findWhere(article.chapters, {"chapterNumber":entries[i].cN})
                subchapter = _.findWhere(chapter.subChapters, {"subChapterNumber":entries[i].scN})
                if (_.findWhere(subchapter, {"scSubChapterNumber":entries[i].sscN}) == null) {
                    subchapter.scSubChapters.push({"chapterNumber":entries[i].cN, "subChapterNumber":entries[i].scN, "scSubChapterNumber":entries[i].sscN, "title":entries[i].sscT, "content":entries[i].sscC});
                }
            }
        };
        

        // Generating .docx file

        var doc = new docx.Document(
            {
                description: "Formatted by Genethesis.io, the free tool for thesis formating.",
                title: article.title
            },
            {
                top: article.marginTop+'cm',
                right: article.marginRight+'cm',
                bottom: article.marginBottom+'cm',
                left: article.marginLeft+'cm'
            }
        );

        // Get language decorator
        lang = article.language.charAt(0).toUpperCase() + article.language.slice(1)
        if (lang == 'Zh') {langAlt = 'Es'}
        if (lang == 'Es') {langAlt = 'Zh'}

        function getFontName(fn) {
            if (fn == 'tnr') {
                fontName = 'Times New Roman'
            }
            if (fn == 'helvetica') {
                fontName = 'Helvetica'
            }
            if (fn == 'arial') {
                fontName = 'Arial'
            }
            if (fn == 'st') {
                fontName = '宋体'
            }
            if (fn == 'ht') {
                fontName = '黑体'
            }
            if (fn == 'fs') {
                fontName = '仿宋'
            }
            return fontName
        };

        function ParagraphRun(text, para) {
            while (text != '') {
                if (text.search('{{') != -1) {
                    runText = text.slice(0, text.search('{{'));
                } else {
                    runText = text;
                }
                // Render the normal text
                if (runText) {
                    para.addRun(new TextRun(runText));
                }

                // If there is a special run
                if (text.search('{{') != -1) {
                    spRun = text.slice(text.search('{{')+2, text.search('}}'));
                    spAttr = spRun.slice(0, spRun.search(':'));
                    spText = spRun.slice(spRun.search(':')+1);
                    if (spAttr == 'bold') {
                        para.addRun(new TextRun(spText).bold());
                    };
                    if (spAttr == 'italic') {
                        para.addRun(new TextRun(spText).italic());
                    };
                    if (spAttr == 'underline') {
                        para.addRun(new TextRun(spText).underline());
                    };
                    if (spAttr == 'bold&italic') {
                        para.addRun(new TextRun(spText).italic().bold());
                    };
                    if (spAttr == 'bold&underline') {
                        para.addRun(new TextRun(spText).bold().underline());
                    };
                    if (spAttr == 'italic&underline') {
                        para.addRun(new TextRun(spText).italic().underline());
                    };
                    if (spAttr == 'bold&italic&underline') {
                        para.addRun(new TextRun(spText).bold().italic().underline());
                    };
                    if (spAttr == 'footnoteAnchor') {
                        spNote = spText.slice(spText.search('footnoteContent:')+16);
                        spText = spText.slice(0, spText.search(', footnoteContent:'));
                        para.addRun(new TextRun(spText)).referenceFootnote(fnrp);
                        doc.createFootnote(new Paragraph(spNote).style('notes'+lang));
                        fnrp = fnrp + 1;
                    };
                }
                // Slice the rest
                if (text.search('}}') != -1){
                    text = text.slice(text.search('}}')+2);
                } else {
                    text = '';
                }
            }
        }

        function ImageRun(run){
            if (run.search('ImageComment') != -1) {
                imgLink = run.slice(14, run.search(', ImageComment'));
                imgComment = run.slice(run.search(', ImageComment')+15, -2)
            } else {
                imgLink = run.slice(14, -3);
                imgComment = '';
            }
            if (fs.existsSync(imgLink)){
                doc.createImage(fs.readFileSync(imgLink), 300, sizeOf(imgLink).height/sizeOf(imgLink).width*300, {
                    floating: {
                        horizontalPosition: {
                            relative: HorizontalPositionRelativeFrom.MARGIN,
                            align: HorizontalPositionAlign.CENTER,
                        },
                        verticalPosition: {
                            relative: VerticalPositionRelativeFrom.PARAGRAPH,
                            offset: 200000,
                        },
                        wrap: {
                            type: TextWrappingType.TOP_AND_BOTTOM,
                        },
                        margins: {
                            top: 0,
                            bottom: 100000,
                        },
                    },
                });
            }
            if (imgComment != '') {
                doc.createParagraph(imgComment).style('imgCmtEs');
            };
        }

        if (lang == 'Es') {
            doc.Styles.createParagraphStyle('TituloZh', '中文标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .font(getFontName(article.sectionTitleFontAlt))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('TituloEs', '西文标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .bold()
                .font(getFontName(article.sectionTitleFont))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('IndexedTituloZh', '中文标题（进入目录）')
                .basedOn("Heading1")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .font(getFontName(article.sectionTitleFontAlt))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('IndexedTituloEs', '西文标题（进入目录）')
                .basedOn("Heading1")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .bold()
                .font(getFontName(article.sectionTitleFont))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('abstractoZh', '中文摘要')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.abstractFontSize * 2)
                .font(getFontName(article.abstractFontAlt))
                .spacing({"line": article.abstractLineSpacing*240})
                .justified()
                .indent({"hanging":-article.abstractFirstIndent*240});
            doc.Styles.createParagraphStyle('abstractoEs', '西文摘要')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.abstractFontSize * 2)
                .font(getFontName(article.abstractFont))
                .spacing({"line": article.abstractLineSpacing*240})
                .justified()
                .indent({"hanging":-article.abstractFirstIndent*240});
            doc.Styles.createParagraphStyle('bibliografiaZh', '中文参考文献')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.bibliographyFontSize * 2)
                .font(getFontName(article.bibliographyFontAlt))
                .spacing({'line': article.bibliographyLineSpacing*240, 'after':article.bibliographyAfterSpacing*240});
            doc.Styles.createParagraphStyle('bibliografiaEs', '西文参考文献')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.bibliographyFontSize * 2)
                .font(getFontName(article.bibliographyFont))
                .spacing({'line': article.bibliographyLineSpacing*240, 'after':article.bibliographyAfterSpacing*240}); 
            doc.Styles.createParagraphStyle('CoverZh', '中文内封面标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.innerCoverFontSize * 2)
                .spacing({"line":article.innerCoverLineSpacing*240})
                .center()
                .font(getFontName(article.innerCoverFontAlt));
            doc.Styles.createParagraphStyle('CoverEs', '西文内封面标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.innerCoverFontSize * 2)
                .spacing({"line":article.innerCoverLineSpacing*240, "before": 5040})
                .center()
                .font(getFontName(article.innerCoverFont));
        }

        if (lang == 'Zh') {
            doc.Styles.createParagraphStyle('TituloZh', '中文标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .font(getFontName(article.sectionTitleFont))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('TituloEs', '西文标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .bold()
                .font(getFontName(article.sectionTitleFontAlt))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('IndexedTituloZh', '中文标题（进入目录）')
                .basedOn("Heading1")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .font(getFontName(article.sectionTitleFont))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('IndexedTituloEs', '西文标题（进入目录）')
                .basedOn("Heading1")
                .next("Body")
                .quickFormat()
                .size(article.sectionTitleFontSize * 2)
                .bold()
                .font(getFontName(article.sectionTitleFontAlt))
                .center()
                .color('000000')
                .spacing({"line": article.sectionTitleLineSpacing*240});
            doc.Styles.createParagraphStyle('abstractoZh', '中文摘要')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.abstractFontSize * 2)
                .font(getFontName(article.abstractFont))
                .spacing({"line": article.abstractLineSpacing*240})
                .justified()
                .indent({"hanging":-article.abstractFirstIndent*240});
            doc.Styles.createParagraphStyle('abstractoEs', '西文摘要')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.abstractFontSize * 2)
                .font(getFontName(article.abstractFontAlt))
                .spacing({"line": article.abstractLineSpacing*240})
                .justified()
                .indent({"hanging":-article.abstractFirstIndent*240});
            doc.Styles.createParagraphStyle('bibliografiaZh', '中文参考文献')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.bibliographyFontSize * 2)
                .font(getFontName(article.bibliographyFont))
                .spacing({'line': article.bibliographyLineSpacing*240, 'after':article.bibliographyAfterSpacing*240});
            doc.Styles.createParagraphStyle('bibliografiaEs', '西文参考文献')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.bibliographyFontSize * 2)
                .font(getFontName(article.bibliographyFontAlt))
                .spacing({'line': article.bibliographyLineSpacing*240, 'after':article.bibliographyAfterSpacing*240}); 
            doc.Styles.createParagraphStyle('CoverZh', '中文内封面标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.innerCoverFontSize * 2)
                .spacing({"line":article.innerCoverLineSpacing*240})
                .center()
                .font(getFontName(article.innerCoverFont));
            doc.Styles.createParagraphStyle('CoverEs', '西文内封面标题')
                .basedOn("Body")
                .next("Body")
                .quickFormat()
                .size(article.innerCoverFontSize * 2)
                .spacing({"line":article.innerCoverLineSpacing*240, "before": 5040})
                .center()
                .font(getFontName(article.innerCoverFontAlt));
        }

        doc.Styles.createParagraphStyle('TituloZh1', '中文一级标题')
            .basedOn("Heading1")
            .next("Body")
            .quickFormat()
            .size(article.title1FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title1LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('TituloEs1', '西文一级标题')
            .basedOn("Heading1")
            .next("Body")
            .quickFormat()
            .size(article.title1FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title1LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('TituloZh2', '中文二级标题')
            .basedOn("Heading2")
            .next("Body")
            .quickFormat()
            .size(article.title2FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title2LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('TituloEs2', '西文二级标题')
            .basedOn("Heading2")
            .next("Body")
            .quickFormat()
            .size(article.title2FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title2LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('TituloZh3', '中文三级标题')
            .basedOn("Heading3")
            .next("Body")
            .quickFormat()
            .size(article.title3FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title3LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('TituloEs3', '西文三级标题')
            .basedOn("Heading3")
            .next("Body")
            .quickFormat()
            .size(article.title3FontSize * 2)
            .font(getFontName(article.titleFont))
            .bold()
            .spacing({"line": article.title3LineSpacing*240})
            .justified()
            .color('000000')
        doc.Styles.createParagraphStyle('cuerpoZh', '中文正文')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.bodyFontSize * 2)
            .font(getFontName(article.bodyFont))
            .spacing({"line": article.bodyLineSpacing*240})
            .justified()
            .indent({"hanging":-article.bodyFirstIndent*240});
        doc.Styles.createParagraphStyle('cuerpoEs', '西文正文')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.bodyFontSize * 2)
            .font(getFontName(article.bodyFont))
            .spacing({"line": article.bodyLineSpacing*240})
            .justified()
            .indent({"hanging":-article.bodyFirstIndent*240});
        doc.Styles.createParagraphStyle('imgCmtZh', '中文图片说明')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.imageCommentFontSize * 2)
            .font(getFontName(article.imageCommentFont))
            .spacing({"line": article.imageCommentLineSpacing*240, "after": 180})
            .center()
        doc.Styles.createParagraphStyle('imgCmtEs', '西文图片说明')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.imageCommentFontSize * 2)
            .font(getFontName(article.imageCommentFont))
            .spacing({"line": article.imageCommentLineSpacing*240, "after": 180})
            .center()
        doc.Styles.createParagraphStyle('notesZh', '中文脚注')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.noteFontSize * 2)
            .font(getFontName(article.noteFont))
        doc.Styles.createParagraphStyle('notesEs', '西文脚注')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.noteFontSize * 2)
            .font(getFontName(article.noteFont))
        //doc.Styles.createParagraphStyle('IndiceZh', '中文目录')
            //.basedOn("Body")
            //.next("Body")
            //.quickFormat()
            //.size(24)
            //.spacing({"line":360})
            //.font('宋体');
        //doc.Styles.createParagraphStyle('IndiceEs', '西文目录')
            //.basedOn("Body")
            //.next("Body")
            //.quickFormat()
            //.size(24)
            //.spacing({"line":360})
            //.font('Times New Roman');
        doc.Styles.createParagraphStyle('toc1', 'TOC 1')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.toc1FontSize * 2)
            .spacing({"line":article.tocLineSpacing*240, "before":article.toc1BeforeSpacing*240})
            .font(getFontName(article.tocFont))
            .indent({"left":article.toc1Indent*240});
        doc.Styles.createParagraphStyle('toc2', 'TOC 2')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.toc2FontSize * 2)
            .spacing({"line":article.tocLineSpacing*240, "before":article.toc2BeforeSpacing*240})
            .font(getFontName(article.tocFont))
            .indent({"left":article.toc2Indent*240});
        doc.Styles.createParagraphStyle('toc3', 'TOC 3')
            .basedOn("Body")
            .next("Body")
            .quickFormat()
            .size(article.toc3FontSize * 2)
            .spacing({"line":article.tocLineSpacing*240})
            .font(getFontName(article.tocFont))
            .indent({"left":article.toc3Indent*240});

        doc.createParagraph(article.title).style('Cover'+lang);
        if (article.titleAlt != ''){
            doc.createParagraph(article.titleAlt).style('Cover'+langAlt);
        }

        const introFooter = doc.createFooter();
        const introPageNumber = new TextRun().pageNumber();
        introFooter.createParagraph().addRun(introPageNumber).center();

        doc.addSection({
            footers: {
                default: introFooter,
            },
            pageNumberStart: 1,
            pageNumberFormatType: PageNumberFormat.UPPER_ROMAN,
        });

        doc.createParagraph('摘要').style('TituloZh').pageBreakBefore();
        a1Cps = article.abstract1.split('\n');
        for (a in a1Cps) {
            if (a1Cps[a].search('ImageAnchor') != -1) {
                ImageRun(a1Cps[a])
            } else {
                p = new Paragraph().style('abstractoZh');
                ParagraphRun(a1Cps[a], p);
                doc.addParagraph(p);
            }
        }
        p = new Paragraph().style('abstractoZh');
        p.addRun(new TextRun('关键词：' + article.keywordsAlt).bold());
        doc.addParagraph(p);

        doc.createParagraph('RESUMEN').style('TituloEs').pageBreakBefore();
        a2Cps = article.abstract2.split('\n');
        for (a in a2Cps) {
            if (a2Cps[a].search('ImageAnchor') != -1) {
                ImageRun(a2Cps[a])
            } else {
                p = new Paragraph().style('abstractoEs');
                ParagraphRun(a2Cps[a], p);
                doc.addParagraph(p);
            }
        }
        p = new Paragraph().style('abstractoEs');
        p.addRun(new TextRun('Palabras claves：' + article.keywords).bold());
        doc.addParagraph(p);

        // Generate Table of Contents
        const toc = new TableOfContents("ÍNDICE", {
            hyperlink: false,
            headingStyleRange: '1-3',
            stylesWithLevels: [new StyleLevel("toc", 1)]
        });   
        if (lang == 'Zh') {
            doc.createParagraph('目录').style('TituloZh').pageBreakBefore();
        }
        if (lang == 'Es') {
            doc.createParagraph('ÍNDICE').style('TituloEs').pageBreakBefore();
        }
        doc.addTableOfContents(toc);

        // Iniciate Footnote count
        fnrp = 1;

        const bodyFooter = doc.createFooter();
        const bodyPageNumber = new TextRun().pageNumber();
        bodyFooter.createParagraph().addRun(bodyPageNumber).center();

        doc.addSection({
            footers: {
                default: bodyFooter,
            },
            pageNumberStart: 1,
            pageNumberFormatType: PageNumberFormat.DECIMAL,
        });

        // Generate Thesis Body
        if (lang == 'Zh') {
            doc.createParagraph('引言').style('TituloZh1').pageBreakBefore();
        }
        if (lang == 'Es') {
            doc.createParagraph('Introducción').style('TituloEs1').pageBreakBefore();
        }
        inps = article.introduction.split('\n');
        for (a in inps) {
            if (inps[a].search('ImageAnchor') != -1) {
                ImageRun(inps[a])
            } else {
                p = new Paragraph().style('cuerpo'+lang);
                ParagraphRun(inps[a], p);
                doc.addParagraph(p);
            }
        }


        for (i in article.chapters) {
            chapter = article.chapters[i];
            doc.createParagraph('').style('Titulo'+lang+'1');
            cT = new Paragraph(chapter.chapterNumber+'. '+chapter.title).style('Titulo'+lang+'1');
            doc.addParagraph(cT);
            if (chapter.content){
                cCps = chapter.content.split('\n');
                for (a in cCps) {
                    if (cCps[a].search('ImageAnchor') != -1) {
                        ImageRun(cCps[a])
                    } else {
                        p = new Paragraph().style('cuerpo'+lang);
                        ParagraphRun(cCps[a], p);
                        doc.addParagraph(p);
                    }
                }
            }
            for (j in chapter.subChapters) {
                subchapter = chapter.subChapters[j];
                scT = new Paragraph(subchapter.chapterNumber+'.'+subchapter.subChapterNumber+'. '+subchapter.title).style('Titulo'+lang+'2');
                doc.addParagraph(scT);
                if (subchapter.content){
                    scCps = subchapter.content.split('\n');
                    for (a in scCps) {
                        if (scCps[a].search('ImageAnchor') != -1) {
                            ImageRun(scCps[a])
                        } else {
                            p = new Paragraph().style('cuerpo'+lang);
                            ParagraphRun(scCps[a], p);
                            doc.addParagraph(p);
                        }
                    }
                }
                for (k in subchapter.scSubChapters) {
                    scsubchapter = subchapter.scSubChapters[k];
                    sscT = new Paragraph(scsubchapter.chapterNumber+'.'+scsubchapter.subChapterNumber+'.'+scsubchapter.scSubChapterNumber+'. '+scsubchapter.title).style('Titulo'+lang+'3');
                    doc.addParagraph(sscT);
                    if (scsubchapter.content){
                        sscCps = scsubchapter.content.split('\n');
                        for (a in sscCps) {
                            if (sscCps[a].search('ImageAnchor') != -1) {
                                ImageRun(sscCps[a])
                            } else {
                                p = new Paragraph().style('cuerpo'+lang);
                                ParagraphRun(sscCps[a], p);
                                doc.addParagraph(p);
                            }
                        }
                    }
                }
                if (subchapter.tailContent){
                    sctCps = subchapter.tailContent.split('\n');
                    for (a in sctCps) {
                        if (sctCps[a].search('ImageAnchor') != -1) {
                            ImageRun(sctCps[a])
                        } else {
                            p = new Paragraph().style('cuerpo'+lang);
                            ParagraphRun(sctCps[a], p);
                            doc.addParagraph(p);
                        }
                    }
                }
            }
            if (chapter.tailContent){
                ctCps = chapter.tailContent.split('\n');
                for (a in ctCps) {
                    if (ctCps[a].search('ImageAnchor') != -1) {
                        ImageRun(ctCps[a])
                    } else {
                        p = new Paragraph().style('cuerpo'+lang);
                        ParagraphRun(ctCps[a], p);
                        doc.addParagraph(p);
                    }
                }
            }
        }

        // Generate Bibliography
        if (lang == 'Zh') {
            doc.createParagraph('参考文献').style('IndexedTituloZh').pageBreakBefore();
        }
        if (lang == 'Es') {
            doc.createParagraph('REFERENCIAS').style('IndexedTituloEs').pageBreakBefore();
        }
        bibps = article.bibliography.split('\n');
        for (i in bibps) {
            num = Number(i) + 1;
            if (bibps[i].split(' ').length > 1) {
                bibg = new Paragraph('('+String(num)+'). '+bibps[i]).style('bibliografiaEs');
            } else {
                bibg = new Paragraph('('+String(num)+'). '+bibps[i]).style('bibliografiaZh');
            }
            doc.addParagraph(bibg);
        }

        // Generate Gratitude
        if (lang == 'Zh') {
            doc.createParagraph('致谢').style('IndexedTituloZh').pageBreakBefore();
        }
        if (lang == 'Es') {
            doc.createParagraph('AGRADECIMIENTOS').style('IndexedTituloEs').pageBreakBefore();
        }
        gps = article.gratitude.split('\n');
        for (a in gps) {
            if (gps[a].search('ImageAnchor') != -1) {
                ImageRun(gps[a])
            } else {
                p = new Paragraph().style('cuerpo'+lang);
                ParagraphRun(gps[a], p);
                doc.addParagraph(p);
            }
        }
        imgLink = '../Genethesis/static/signatures/'+String(article.authorID)+'.png';
        if (fs.existsSync(imgLink)){
            doc.createImage(fs.readFileSync(imgLink), 200, sizeOf(imgLink).height/sizeOf(imgLink).width*200, {
                floating: {
                    horizontalPosition: {
                        relative: HorizontalPositionRelativeFrom.MARGIN,
                        align: HorizontalPositionAlign.RIGHT,
                    },
                    verticalPosition: {
                        relative: VerticalPositionRelativeFrom.PARAGRAPH,
                        offset: 200000,
                    },
                    wrap: {
                        type: TextWrappingType.TOP_AND_BOTTOM,
                    },
                    margins: {
                        top: 0,
                        bottom: 0,
                    },
                },
            });
        }

        // Used to export the file into a .docx file
        const packer = new Packer();
        filePath = "../Genethesis/static/articles/"+String(article.authorID)+"/"+String(article.id)+"/"+"thesis.docx"
        pdfPath = "../Genethesis/static/articles/"+String(article.authorID)+"/"+String(article.id)+"/"+"thesis.pdf"
        packer.toBuffer(doc).then((buffer) => {
            fs.writeFileSync(filePath, buffer);
        });


        res.send(filePath.slice(13));
    });
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))