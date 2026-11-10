<script setup>
import { computed, onMounted, ref } from 'vue'
import { createTask, deleteTask, listTasks, updateTask } from './api'

const tasks = ref([])
const title = ref('')
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const remaining = computed(() => tasks.value.filter((task) => !task.done).length)

async function refresh() {
  loading.value = true
  error.value = ''
  try {
    tasks.value = await listTasks()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

async function add() {
  const value = title.value.trim()
  if (!value || saving.value) return
  saving.value = true
  error.value = ''
  try {
    await createTask(value)
    title.value = ''
    await refresh()
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

async function toggle(task) {
  try {
    await updateTask(task.id, !task.done)
    await refresh()
  } catch (err) {
    error.value = err.message
  }
}

async function remove(task) {
  try {
    await deleteTask(task.id)
    await refresh()
  } catch (err) {
    error.value = err.message
  }
}

onMounted(refresh)
</script>

<template>
  <main>
    <h1>待办清单</h1>
    <p>未完成 {{ remaining }} 项</p>
    <form @submit.prevent="add">
      <input v-model="title" maxlength="100" placeholder="输入新任务" aria-label="任务标题" />
      <button :disabled="!title.trim() || saving">{{ saving ? '保存中…' : '添加' }}</button>
    </form>
    <p v-if="error" role="alert">{{ error }}</p>
    <p v-if="loading">加载中…</p>
    <p v-else-if="tasks.length === 0">还没有任务</p>
    <ul v-else>
      <li v-for="task in tasks" :key="task.id">
        <label>
          <input type="checkbox" :checked="task.done" @change="toggle(task)" />
          <span :class="{ done: task.done }">{{ task.title }}</span>
        </label>
        <button type="button" @click="remove(task)">删除</button>
      </li>
    </ul>
  </main>
</template>
