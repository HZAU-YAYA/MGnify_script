while read -r line; do
genome=$(echo "$line" | awk -F'\t' '{print $1}')
ftp_link=$(echo "$line" | awk -F'\t' '{print $3}')
mkdir /public/home/byxu/Work/project/human_gut/UHGG_Bifidobacterium/work/${genome}
cd /public/home/byxu/Work/project/human_gut/UHGG_Bifidobacterium/work/${genome}/
wget -c ${ftp_link}
done < id_taxonmy_ftp.txt
