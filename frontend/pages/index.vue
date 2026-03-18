<template>
  <div class="min-h-screen">
    <AppHeader />
    
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute z-1  inset-[50px] size-[500px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute inset-[550px] to blur-[100px] size-[800px] rounded-full
      bg-radial from-primary from-20% to-secondary opacity-100 animate-pulse"></div>
      <div class="absolute z-1 inset-[50px] size-[500px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute inset-[125px] blur-[10px] left-[1700px] size-[500px] rounded-full
      bg-radial from-primary from-10% to-secondary opacity-60"></div>
      <div class="z-10 text-center">
        <h1 class="text-6xl font-bold font-heading text-white">In silico симулятор взаимодействия молекул</h1>
        <NuxtLink to="/editor" class="bg-primary px-8 py-4 rounded-full text-xl font-bold hover:opacity-90 transition">
          Начать
        </NuxtLink>
      </div>
    </section>

    <section class="py-20 bg-secondary relative">
      <div class="absolute inset-0 opacity-10" style="background-image: url('~/assets/media/logo.svg'); background-size: 100px; transform: rotate(45deg);"></div>
      <div class="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 relative z-10">
        <div class="carousel">
          <div class="bg-gray-800 h-64 rounded-lg flex items-center justify-center">Фото 1</div>
          <div class="bg-gray-800 h-64 rounded-lg flex items-center justify-center">Фото 2</div>
          <div class="bg-gray-800 h-64 rounded-lg flex items-center justify-center">Фото 3</div>
        </div>
        <div>
          <h2 class="text-4xl mb-4">О проекте</h2>
          <p class="text-lg">
            Разработка веб-платформы для визуализации уровня безопасности взаимодействия соединений лекарственных препаратов и биологических мишеней.
          </p>
        </div>
      </div>
    </section>

    <section class="py-20 bg-primary relative">
      <div class="absolute inset-0 opacity-10" style="background-image: url('~/assets/media/logo.svg'); background-size: 100px; transform: rotate(45deg);"></div>
      <div class="container mx-auto relative z-10">
        <h2 class="text-4xl mb-10 text-center">Партнеры</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div v-for="i in 4" :key="i" class="bg-black h-32 rounded flex items-center justify-center">Партнер {{ i }}</div>
        </div>
      </div>
    </section>

    <section class="py-20 bg-gradient-main">
      <div class="container mx-auto">
        <h2 class="text-4xl mb-10 text-center">Часто задаваемые вопросы</h2>
        <div class="max-w-2xl mx-auto space-y-4">
          <details class="bg-primary p-4 rounded cursor-pointer">
            <summary class="font-bold">Как работает модель?</summary>
            <p class="mt-2">Используются методы MLP, ChemBERTa и Morgan fingerprint.</p>
          </details>
          <details class="bg-primary p-4 rounded cursor-pointer">
            <summary class="font-bold">Какие данные используются?</summary>
            <p class="mt-2">База данных ChEMBL.</p>
          </details>
          <details class="bg-primary p-4 rounded cursor-pointer">
            <summary class="font-bold">Можно ли экспортировать результаты?</summary>
            <p class="mt-2">Да, доступны форматы PDF, Excel, TXT.</p>
          </details>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>