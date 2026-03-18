<template>
  <div class="flex flex-col items-center justify-center min-h-screen">
    <AppHeader />
    
    <section class="relative w-full h-screen flex items-center justify-center overflow-hidden z-[5]">
      <div class="absolute inset-[-50px] size-[500px] blur-[10px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute inset-[550px] to blur-[100px] size-[800px] rounded-full
      bg-radial from-primary from-20% to-secondary opacity-100 animate-pulse"></div>
      <div class="absolute inset-[25px] size-[500px] blur-[50px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute inset-[175px] blur-[25px] left-[1300px] size-[350px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-60"></div>
      <div class="z-10 text-center">
        <h1 class="text-6xl md:text-7xl font-bold">In silico симулятор <br> взаимодействия молекул</h1>
        <NuxtLink to="/editor" class="bg-primary text-white px-[10px] py-[5px] rounded-[20px] text-xl hover:opacity-90 transition">
          Начать
        </NuxtLink>
      </div>
    </section>

    <section class="w-full h-screen bg-secondary relative text-center" id="about">
      <div class="container mx-auto grid grid-cols-1 md:grid-cols-2 gap-10 relative z-10">
        <div>
          <h2 class="text-4xl mb-[75px] font-heading">О проекте</h2>
          <p class="text-xl font-sans mb-[65px]">
            Наш проект направлен на использование технологий machine learning и deep learning для предсказания in silico вероятности активности ряда биомишеней, отвечающих за наличие у соединения болеутоляющих и противовоспалительных свойств, в целях оптимизации in vivo доклинических испытаний и уменьшения числа экспериментов на животных путём проверки только тех соединений, которые с наибольшей вероятностью обладают полезными фармакологическими свойствами. Методы машинного обучения при корректной постановке задачи и валидации демонстрируют высокую предиктивную способность и не требуют значительных вычислительных ресурсов для получения предсказания после этапа обучения, благодаря чему такая модель может при минимальных затратах существенно сократить число испытаний, отсеивая неэффективные соединения.
          </p>

          <p class="text-xl font-sans">
            Основная <span class="font-bold">цель</span> проекта — создание эффективного инструмента для биологов и специалистов по разработке лекарственных средств, позволяющего повысить эффективность разработки за счёт сокращения числа необходимых экспериментальных испытаний. Перспективы развития включают обучение более мощных моделей, расширение набора данных и дообучение модели на результатах испытаний новых химических соединений
          </p>
        </div>
      </div>
    </section>

    <section class="w-full h-screen bg-primary relative" id="partners">
      <div class="container mx-auto relative z-10 text-center">
        <h2 class="text-4xl mb-10 text-center">Наши партнеры</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-y-[300px]">
          <p class="text-xl">ЛГМУ им. Святителя Луки</p>
          <p class="text-xl">Городская больница № 7</p>
          <p class="text-xl">МинЗдрав ЛНР</p>
          <p class="text-xl">МинОбрНауки ЛНР</p>
        </div>
      </div>
    </section>

    <section class="w-full h-screen relative overflow-hidden" id="faq">
      <div class="absolute -z-10 inset-[-50px] size-[500px] blur-[10px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute -z-10 inset-[550px] to blur-[100px] size-[800px] rounded-full
      bg-radial from-primary from-20% to-secondary opacity-100 animate-pulse"></div>
      <div class="absolute -z-10 inset-[25px] size-[500px] blur-[50px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-20"></div>
      <div class="absolute -z-10 inset-[175px] blur-[25px] left-[1300px] size-[350px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-60"></div>
      <div class="z-10 mx-auto">
        <h2 class="text-4xl mb-[125px] text-center">Часто задаваемые вопросы</h2>
        <div class="max-w-[65%] mx-auto space-y-[10px]">
          <details class="bg-primary p-[10px] rounded-[10px] cursor-pointer">
            <summary class="font-bold font-sans text-md">Как работает модель?</summary>
            <p>Используются методы MLP, ChemBERTa и Morgan fingerprint.</p>
          </details>
          <details class="bg-primary p-[10px] rounded-[10px] cursor-pointer">
            <summary class="font-bold font-sans text-md">Какие данные используются?</summary>
            <p>База данных ChEMBL, Uniprot и другие.</p>
          </details>
          <details class="bg-primary p-[10px] rounded-[10px] cursor-pointer">
            <summary class="font-bold font-sans text-md">Можно ли экспортировать результаты?</summary>
            <p>Да, доступны форматы PDF, Excel, TXT.</p>
          </details>
        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>