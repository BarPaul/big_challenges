<template>
  <div class="min-h-screen flex flex-col">
    <AppHeader />
    
    <section class="flex-1 bg-gradient-main p-10">
      <div class="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-10">
        <!-- Форма -->
        <div>
          <h2 class="text-4xl mb-6">Симулировать молекулу</h2>
          <textarea 
            v-model="smiles" 
            placeholder="Введите SMILES..." 
            class="w-full h-32 bg-black bg-opacity-50 rounded p-4 text-white mb-4"
          ></textarea>
          <button 
            @click="simulate" 
            :disabled="loading"
            class="bg-primary px-6 py-3 rounded font-bold w-full"
          >
            {{ loading ? 'Загрузка...' : 'Симулировать' }}
          </button>
        </div>

        <!-- 2D Редактор (Самописный скелет) -->
        <div class="bg-black bg-opacity-50 rounded p-4 relative">
          <h3 class="mb-4">2D Структура</h3>
          <canvas ref="canvas" class="w-full h-64 border border-gray-600"></canvas>
          <p class="text-xs mt-2 text-gray-400">*Для полноценной визуализации требуется интеграция RDKit.js</p>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup>
const smiles = ref('')
const loading = ref(false)
const router = useRouter()

const simulate = async () => {
  if (!smiles.value) return
  loading.value = true
  try {
    // Отправка на backend
    await $fetch('/api/predict-biotargets', {
      method: 'POST',
      body: { smiles: smiles.value }
    })
    // Переход на страницу результатов (в реальном_app нужно передавать данные)
    router.push('/result') 
  } catch (e) {
    alert('Ошибка симуляции')
  } finally {
    loading.value = false
  }
}

// Простая отрисовка на canvas (заглушка)
onMounted(() => {
  const ctx = document.querySelector('canvas').getContext('2d')
  ctx.fillStyle = '#fff'
  ctx.fillText('Молекула', 50, 50)
})
</script>