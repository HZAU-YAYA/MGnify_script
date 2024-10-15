python download_MGnify.py --path /home/xuboya/Work/database/genmoes_db/MGnify/genomes --input all_genome_genome.tsv --threads 20 #下载基因组


#检查下载结果
for i in $(find /home/xuboya/Work/database/genmoes_db/MGnify/genomes/MAG/ -type f -empty)
do
n1=$(basename ${i})
prefix=$(echo ${n1} | cut -d. -f1)
path=$(dirname ${n1})
cd ${path}
url=$(awk -F'\t' -v prefix="${prefix}" '$1 == prefix {print $4}' /home/xuboya/Work/database/genmoes_db/MGnify/all_genome_genome.tsv)
echo "${url}"
done
for i in $(find /home/xuboya/Work/database/genmoes_db/MGnify/genomes/MAG/ -type f -empty)
do
n1=$(basename ${i})
prefix=$(echo ${n1} | cut -d. -f1)
path=$(dirname ${n1})
cd ${path}
url=$(awk -F'\t' -v prefix="${prefix}" '$1 == prefix {print $4}' /home/xuboya/Work/database/genmoes_db/MGnify/all_genome_genome.tsv)
if [ -n "$url" ]; then
        wget -O ${i} ${url}
    else
        echo "URL not found for prefix ${prefix}"
    fi
done
