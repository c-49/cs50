<template>
    <div class="mt-4">
        <el-input v-model="text" :disabled="loading" type="textarea" autosize style="width: 400px" placeholder="Text to analyze..." class="input-with-select"/>
        <el-button :icon="Select" @click="analyzeSentiment"/>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Select } from '@element-plus/icons-vue'

const emit = defineEmits(['on-analyzed'])

const text = ref('')
const loading = ref(false)

const analyzeSentiment = async () => {
    try {
        loading.value = true
        const response = await fetch('http://127.0.0.1:5000/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text.value })
        })
        const result = await response.json()
        emit('on-analyzed', result[0], text.value)
        text.value = ''
    } catch (error) {
        console.error('Error:', error)
    }
    loading.value = false
}
</script>
