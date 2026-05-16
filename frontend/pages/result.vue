<template>
  <div class="min-h-screen flex flex-col items-center">
    <AppHeader />
    
    <section class="flex-1 bg-gradient-main p-6 md:p-10">
      <div class="container mx-auto max-w-6xl">
        
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <h2 class="text-3xl md:text-4xl font-bold text-white">Результаты симуляции</h2>

          <button 
            @click="$router.push('/editor')"
            class="px-[8px] py-[2px] bg-primary hover:bg-primary/80 hover:text-white/80 rounded-[20px] text-white border-none mb-[20px] font-sans text-md"
          >
            ← Назад к редактору
          </button>
        </div>

        <div v-if="!prediction" class="text-center py-[20px] bg-white/20 rounded-[50px] border border-white">
          <div class="text-6xl mb-[10px] mt-[10px]">🧪</div>
          <h3 class="text-xl font-bold text-gray-200 mb-2">Нет данных для отображения</h3>
          <p class="text-gray-400 mb-6">Вы еще не провели симуляцию или данные были очищены.</p>
          <button 
            @click="$router.push('/editor')"
            class="px-[10px] py-[5px] bg-primary hover:bg-primary/40 rounded-full font-bold font-sans text-white transition border-none mb-[20px]"
          >
            Перейти к редактору
          </button>
        </div>

        <div v-else class="space-y-8">
          
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            
            <div class="bg-white rounded-[20px] p-5 flex flex-col mb-[10px]">
              <div class="flex-1 bg-black/40 rounded-lg relative overflow-hidden min-h-[250px] flex items-center justify-center">
                <div ref="molContainer" class="w-full h-full"></div>
                <div v-if="!smiles" class="absolute inset-0 flex items-center justify-center text-gray-500 text-sm">
                  Нет данных SMILES
                </div>
              </div>
              <div class="mt-3 text-xs text-gray-500 font-sans break-all text-center">
                {{ smiles || '—' }}
              </div>
            </div>

          </div>

          <div class="bg-gray-900/50 border-none overflow-hidden">
            <div class="p-5 border-none flex justify-between items-center">
              <h3 class="text-lg font-bold text-white">Полный список мишеней</h3>
              <button 
                @click="downloadCSV"
                class="text-sm px-[15px] py-[10px] bg-secondary font-sans hover:bg-secondary/60 rounded-full text-white text-xs flex"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                </svg>
                CSV
              </button>
            </div>
            
            <div class="overflow-x-auto">
              <table class="w-full text-left bg-white border-collapse rounded-[10px]">
                <thead>
                  <tr class="text-gray-400 text-xs uppercase tracking-wider">
                    <th class="p-[4px] font-bold font-heading text-primary">Мишень</th>
                    <th class="p-[4px] font-bold font-heading text-primary">UniProt ID</th>
                    <th class="p-[4px] font-bold font-heading text-primary">ChEMBL ID</th>
                    <th class="p-[4px] font-bold font-heading text-primary text-right">Вероятность</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-800">
                  <tr v-for="(row, i) in prediction.table" :key="i" class="hover:bg-gray-800/30 transition-colors group">
                    <td class="p-4">
                      <div class="font-medium font-sans text-dark">{{ row.target_name }}</div>
                    </td>
                    <td class="p-4">
                      <a :href="`https://www.uniprot.org/uniprot/${row.uniprot_id}`" target="_blank" 
                         class="text-secondary hover:text-secondary/50 underline decoration-blue-400/30 hover:decoration-blue-300 transition-all font-sans text-sm">
                        {{ row.uniprot_id }}
                      </a>
                    </td>
                    <td class="p-4">
                      <a :href="`https://www.ebi.ac.uk/chembl/target_report_card/${row.chembl_id}/`" target="_blank" 
                         class="text-secondary hover:text-secondary/50 underline decoration-purple-400/30 hover:decoration-purple-300 transition-all font-sans text-sm">
                        {{ row.chembl_id }}
                      </a>
                    </td>
                    <td class="p-4 text-right">
                      <div class="inline-flex items-center gap-2">
                        <div class="w-16 bg-gray-700 h-1.5 rounded-full overflow-hidden">
                          <div 
                            class="h-full rounded-full"
                            :class="{
                              'bg-green': row.chance > 0.2,
                              'bg-yellow': row.chance > 0.05 && row.chance <= 0.2,
                              'bg-gray-300': row.chance <= 0.05
                            }"
                            :style="{ width: (row.chance * 100) + '%' }"
                          ></div>
                        </div>
                        <span class="font-sans text-sm text-dark w-12 inline-block">
                          {{ (row.chance * 100).toFixed(2) }}%
                        </span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>

          <p class="text-gray-400 mt-1" v-if="prediction?.id">
            ID запроса: <span class="font-sans text-sm bg-gray-800 px-2 py-1 rounded">{{ prediction.id }}</span>
          </p>

        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import * as OCL from 'openchemlib'

const prediction = ref<any>(null)
const smiles = ref<string>('')
const molContainer = ref<HTMLDivElement | null>(null)


const drawMolecule = async () => {
  if (!smiles.value || !molContainer.value) return
  
  try {
    molContainer.value.innerHTML = ''
    

    const mol = OCL.Molecule.fromSmiles(smiles.value)
    if (!mol) throw new Error('Invalid SMILES')
    
    mol.ensureHelperArrays(OCL.Molecule.cHelperNeighbours)
    
    const width = molContainer.value.clientWidth || 400
    const height = molContainer.value.clientHeight || 300
        
    molContainer.value.innerHTML = mol.toSVG(width, height)
  } catch (e) {
    console.error('Ошибка отрисовки молекулы:', e)
    if (molContainer.value) {
      molContainer.value.innerHTML = '<div class="text-red-400 text-sm">Ошибка структуры</div>'
    }
  }
}


const downloadCSV = () => {
  if (!prediction.value?.table) return
  
  const headers = ['Target Name', 'UniProt ID', 'ChEMBL ID', 'Chance']
  const rows = prediction.value.table.map((row: any) => [
    `"${row.target_name}"`,
    row.uniprot_id,
    row.chembl_id,
    row.chance
  ])
  
  const csvContent = [
    headers.join(','),
    ...rows.map(r => r.join(','))
  ].join('\n')
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  const url = URL.createObjectURL(blob)
  
  link.setAttribute('href', url)
  link.setAttribute('download', `prediction_${prediction.value.id || 'result'}.csv`)
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  const raw = localStorage.getItem('lastPrediction')
  const lastSmiles = localStorage.getItem('lastSmiles')
  
  if (raw) {
    try {
      prediction.value = JSON.parse(raw)
      smiles.value = lastSmiles || '' 
      
      nextTick(() => {
        drawMolecule()
      })
    } catch (e) {
      console.error('Ошибка парсинга данных:', e)
    }
  }
})
</script>
