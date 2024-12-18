<template>
  <div class="min-h-screen bg-gray-100 flex flex-col justify-center overflow-hidden">
    <div class="relative py-3 w-2xl sm:mx-auto">
      <div class="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
      <div class="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
        <div class="mx-auto">
          <div>
            <h1 class="text-2xl font-semibold">POC 测试工具</h1>
          </div>
          <div class="divide-y divide-gray-200">
            <div class="text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div class="relative">
                  <a-input v-model:value="url" placeholder="输入 URL" />
                </div>
                <div class="relative mt-6">
                  <a-button type="primary" @click.prevent="startTest"
                    :disabled="isLoading">{{ isLoading ? '测试中...' : '开始测试' }}</a-button>
                </div>
            </div>
            <div class="text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
              <h2 class="text-xl font-semibold mb-4">检测到的漏洞</h2>
              <div v-if="vulnerabilities.length === 0 && !isLoading" class="text-gray-500">
                尚未检测到漏洞。
              </div>
              <ul v-else class="space-y-4 overflow-y-auto max-h-xs">
                <li v-for="(vuln, index) in vulnerabilities" :key="index" class="bg-gray-50 p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <div>
                      <span class="font-medium">{{ vuln.name }}</span>
                      <p class="text-sm text-gray-500">{{ vuln.script }}</p>
                    </div>
                    <a-button danger @click.prevent="attack(vuln)" :disabled="canAttack.includes(vuln.script)"> {{ canAttack.includes(vuln.script) ? '攻击' : '暂不支持攻击' }} </a-button>
                  </div>
                  <p class="text-sm text-gray-600 mt-2">{{ vuln.description }}</p>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <contextHolder />
</template>

<script setup>
import { ref } from 'vue'
import { invoke } from '@tauri-apps/api/core';
import { notification } from 'ant-design-vue';

const [api, contextHolder] = notification.useNotification();
const openNotification = (message, description, type = 'info') => {
  api[type]({
    message,
    description,
    placement: 'topRight',
  });
};
const url = ref('http://49.233.1.139:7001')
const vulnerabilities = ref([])
const isLoading = ref(false)
const canAttack = ref(['CVE_2021_36749.py', 'CVE_2021_42013.py', 'tomcat_weakpass_getshell.py'])

const parseVulnerabilities = (response) => {
  vulnerabilities.value = [];
  const regex = /\[!\] Name: (.*?)\s+Script: (.*?)\s+/gs;
  let match;
  while ((match = regex.exec(response)) !== null) {
    vulnerabilities.value.push({
      name: match[1],
      script: match[2]
    });
  }
};

const startTest = async () => {
  isLoading.value = true
  vulnerabilities.value = []
  try {
    const res = await invoke('run_python', {
      invokeMessage: `-u,${url.value}`
    });
    console.log(res)
    parseVulnerabilities(res)
    console.log('漏洞:', vulnerabilities.value)
    openNotification('测试成功', '', 'success')
  } catch (error) {
    console.error('错误:', error)
    openNotification('测试错误', '测试时发生错误。请再试一次。', 'error')
  } finally {
    isLoading.value = false
  }
}

const attack = async(vulnerability) => {
  try {
    const res = await invoke('run_python', {
      invokeMessage: `-u,${url.value},-p,${vulnerability.script},--attack`
    });
    if (res.includes('ERROR')) {
      openNotification('攻击失败', '攻击时发生错误。请再试一次。', 'error')
    } else {
      openNotification('攻击成功', '', 'success')
    }
  } catch (error) {
    console.error('错误:', error)
    openNotification('攻击错误', '测试时发生错误。请再试一次。', 'error')
  }
}
</script>