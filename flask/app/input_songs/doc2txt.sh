# converts doc/docx files to raw text
unzip -p $1 word/document.xml | sed -e 's/<\/w:p>/\n/g; s/<[^>]\{1,\}>//g; s/[^[:print:]\n]\{1,\}//g' > $2
