import aiohttp
import asyncio
import backoff

@backoff.on_exception(backoff.expo, aiohttp.ClientError, max_tries=10)
async def fetch(session, url):
    async with session.get(url, timeout=100) as response:
        return await response.json()

async def create_task(session, genome):
    download_url = genome['relationships']['downloads']['links']['related']
    return genome, await fetch(session, download_url)

async def run_url(pre):
    all_data = {}
    mgnify_url_genomes = 'https://www.ebi.ac.uk/metagenomics/api/v1/genomes'
    async with aiohttp.ClientSession() as session:
        genomes_data = await fetch(session, mgnify_url_genomes)

        while True:
            tasks = []
            for genome in genomes_data['data']:
                tasks.append(create_task(session, genome))

            responses = await asyncio.gather(*tasks)
            for (genome, download_data) in responses:
                genome_accession = genome['attributes']['accession']
                taxon = genome['attributes']['taxon-lineage']
                genomes_type = genome['attributes']['type']
                fna_url = next((l['links']['self'] for l in download_data['data']
                                if l['type'] == 'genome-downloads' and l['id'] == genome_accession + '.fna'), None)
                if fna_url:
                    all_data[genome_accession] = [genomes_type, taxon, fna_url]
                    print(genome_accession, genomes_type, taxon, fna_url)

            next_page = genomes_data['links'].get('next')
            if not next_page:
                break
            genomes_data = await fetch(session, next_page)

    with open(pre + '_genome.tsv', 'w') as f:
        f.write('Genome_accession\tGenome_type\tTaxon\tFNA_URL\n')
        for genome_accession, data in all_data.items():
            f.write(f"{genome_accession}\t{data[0]}\t{data[1]}\t{data[2]}\n")

    return all_data

# 运行异步函数
if __name__ == '__main__':
    asyncio.run(run_url('all_genome'))
