<script setup>
import ToneAnalyzer from './components/ToneAnalyzer.vue'
import { h } from 'vue'
import { ElNotification } from 'element-plus'

const createNotif = (res, text) => {
  const response = res[0]
  ElNotification({
    title: `${response.label} - ${(response.score * 100).toFixed(2)}%`,
    message: h('i', { style: `color: ${ response.label === 'NEGATIVE' ? 'red' : 'green'}` }, text),
    duration: 0,
  })
}
</script>

<template>
  <div class="center-screen">
    <div class="content">
      <div class="header-text">Tone Analyzer</div>
      <tone-analyzer @on-analyzed="createNotif"/>
    </div>
  </div>
</template>

<style scoped>
.center-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* Full viewport height */
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.header-text {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}
</style>
