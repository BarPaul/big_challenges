<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    
    <section class="flex-1 p-10">
      <div class="container mx-auto">
        <h2 class="text-4xl mb-10">Результаты</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10 mb-10">
          <!-- Визуализация -->
          <div class="bg-gray-800 p-4 rounded">
            <h3 class="mb-4">Структура</h3>
            <div class="h-64 bg-black flex items-center justify-center">Изображение молекулы</div>
          </div>
          
          <!-- Диаграмма -->
          <div class="bg-gray-800 p-4 rounded col-span-2">
            <h3 class="mb-4">Соотношение классов</h3>
            <div class="h-64 flex items-center justify-center">График (Chart.js / D3.js)</div>
          </div>
        </div>

        <!-- Таблица -->
        <div class="bg-gray-800 p-4 rounded mb-10 overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="border-b border-gray-600">
                <th class="p-3">Мишень</th>
                <th class="p-3">Класс</th>
                <th class="p-3">UniProt</th>
                <th class="p-3">ChEMBL</th>
                <th class="p-3">Вероятность</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in results" :key="i" class="border-b border-gray-700">
                <td class="p-3">{{ row.target }} ({{ row.common_name }})</td>
                <td class="p-3">{{ row.target_class }}</td>
                <td class="p-3">
                  <a :href="`https://www.uniprot.org/uniprot/${row.uniprot_id}`" target="_blank" class="text-primary underline">
                    {{ row.uniprot_id }}
                  </a>
                </td>
                <td class="p-3">
                  <a :href="`https://www.ebi.ac.uk/chembl/entity/${row.chEMBL_id}`" target="_blank" class="text-primary underline">
                    {{ row.chEMBL_id }}
                  </a>
                </td>
                <td class="p-3 w-48">
                  <div class="bg-gray-600 h-4 rounded overflow-hidden">
                    <div class="bg-primary h-full" :style="{ width: (row.probability * 100) + '%' }"></div>
                  </div>
                  <span class="text-xs">{{ (row.probability * 100).toFixed(1) }}%</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Кнопки экспорта -->
        <div class="flex gap-4">
          <button class="bg-secondary px-6 py-2 rounded">Скачать PDF</button>
          <button class="bg-secondary px-6 py-2 rounded">Скачать Excel</button>
          <button class="bg-secondary px-6 py-2 rounded">Скачать TXT</button>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup>
// Данные заглушки, в реальности приходят с бэкенда
const results = ref([
  {
    target: "COX-2",
    common_name: "Cyclooxygenase-2",
    uniprot_id: "P35354",
    chEMBL_id: "CHEMBL228",
    probability: 0.95,
    target_class: "Enzyme"
  }
])
</script>