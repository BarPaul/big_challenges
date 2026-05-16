<template>
  <div class="min-h-screen flex flex-col items-center">
    <AppHeader />

    <div class="max-w-full overflow-hidden">
      <div class="absolute inset-[-150px] size-[500px] blur-[10px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-60 z-[-1] "></div>
      <div class="absolute inset-[450px] left-[800px] size-[700px] blur-[15px] rounded-full
      bg-radial from-secondary from-10% to-primary opacity-40 z-[-1]"></div>
    </div>

    <section class="flex-1 bg-gradient-main p-4 sm:p-6 mt-[20px]">
      
      <div class="container mx-auto max-w-5xl">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          
          <div>
            <h2 class="text-2xl sm:text-3xl font-bold mb-4">Симулировать молекулу</h2>
            
            <div class="flex flex-wrap gap-2 mb-3">
              <button v-for="atom in atomList" :key="atom"
                @click="selectedAtom = atom"
                :class="['min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm font-bold border transition rounded-[20px] ml-[10px] text-base font-sans', 
                         selectedAtom === atom ? 'bg-primary border-primary text-white' : 'bg-gray-800 border-gray-600 hover:bg-gray-700']">
                {{ atom }}
              </button>
            </div>
            
            <div class="flex flex-wrap gap-2 mb-4">
              <button @click="selectedBondType = 'single'" :class="['min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm border transition rounded-[3px] ml-[10px] text-base font-sans mb-[20px] mt-[10px]', selectedBondType === 'single' ? 'bg-primary border-primary text-white' : 'bg-gray-800 border-gray-600 hover:bg-gray-700']">─</button>
              <button @click="selectedBondType = 'double'" :class="['min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm border transition rounded-[3px] ml-[10px] text-base font-sans mb-[20px] mt-[10px]', selectedBondType === 'double' ? 'bg-primary border-primary text-white' : 'bg-gray-800 border-gray-600 hover:bg-gray-700']">═</button>
              <button @click="selectedBondType = 'triple'" :class="['min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm border transition rounded-[3px] ml-[10px] text-base font-sans mb-[20px] mt-[10px]', selectedBondType === 'triple' ? 'bg-primary border-primary text-white' : 'bg-gray-800 border-gray-600 hover:bg-gray-700']">≡</button>
              
              <div class="h-6 w-px bg-gray-700 mx-1 hidden sm:block"></div>
              
              <button @click="addCycle(5)" class="min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm bg-purple-900/50 border border-purple-700 hover:bg-purple-900 transition rounded-[3px] ml-[10px] text-base font-sans mb-[20px] mt-[10px]">⬠</button>
              <button @click="addCycle(6, true)" class="min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm bg-purple-900/50 border border-purple-700 hover:bg-purple-900 transition rounded-[3px] ml-[10px] text-base font-sans mb-[20px] mt-[10px]">⬡</button>
              
              <div class="h-6 w-px bg-gray-700 mx-1 hidden sm:block"></div>
              <button @click="clearCanvas" class="min-h-[40px] px-2.5 py-1.5 rounded text-xs sm:text-sm bg-gray-800 border border-gray-600 hover:bg-gray-700 transition rounded-[3px] ml-[10px] text-base font-sans text-white bg-red mb-[20px] mt-[10px]">✕</button>
            </div>
            
            <div ref="canvasRef"
              class="w-full h-64 sm:h-80 md:h-96 lg:h-[420px] bg-white/10 rounded-[50px] border border-gray-700 relative select-none touch-none overflow-hidden"
              @mousedown.prevent="handleStart"
              @mousemove="handleMove"
              @mouseup="handleEnd"
              @mouseleave="handleLeave"
              @touchstart.prevent="handleStart"
              @touchmove.prevent="handleMove"
              @touchend.prevent="handleEnd">
              
              <svg class="w-full h-full" viewBox="0 0 800 400" preserveAspectRatio="xMidYMid meet">
                <rect v-if="isSelecting && selectRect"
                  :x="selectRect.x" :y="selectRect.y" :width="selectRect.w" :height="selectRect.h"
                  fill="rgba(59, 130, 246, 0.15)" stroke="#3b82f6" stroke-width="1.5" stroke-dasharray="4,3" />

                <g v-for="b in bondsDisplay" :key="'b'+b.id" class="cursor-pointer">
                  <line v-for="(l, i) in b.lines" :key="i"
                    :x1="l.x1" :y1="l.y1" :x2="l.x2" :y2="l.y2"
                    :stroke="b.isSelected ? '#f59e0b' : '#94a3b8'"
                    :stroke-width="b.isSelected ? 3.5 : 2.5" />
                </g>
                
                <g v-for="atom in atoms" :key="'a'+atom.id">
                  <circle :cx="atom.x" :cy="atom.y" r="18" 
                    :fill="atomColors[atom.symbol]?.bg || '#475569'"
                    :stroke="selectedAtomIds.includes(atom.id) ? '#f59e0b' : '#64748b'"
                    :stroke-width="selectedAtomIds.includes(atom.id) ? 3 : 2.5" />
                  <text :x="atom.x" :y="atom.y + 5" text-anchor="middle" class="fill-white font-sans text-sm pointer-events-none select-none">
                    {{ atom.symbol }}
                  </text>
                </g>
              </svg>
              
            </div>
            
            <div class="mt-4">
              <label class="block text-sm text-gray-300 font-sans text-md mt-[5px] mb-[5px]">Smiles:</label>
              <input v-model="smiles"
                class="w-full min-h-[44px] bg-gray-900 border border-gray-700 rounded-[12px] px-3 py-2 text-dark text-base font-sans sm:text-base focus:outline-none focus:ring-2 focus:ring-primary mb-[5px]" />
              
              <div v-if="validationMsg" :class="['mt-2 text-sm flex items-center gap-1 mb-[5px]', validationStatus === 'error' ? 'text-red-400' : 'text-green-400']">
                <span>{{ validationStatus === 'error' ? '❌' : validationStatus === 'warning' ? '⚠️' : '✅' }}</span>
                <span>{{ validationMsg }}</span>
              </div>
            </div>
            
            <button @click="simulate" :disabled="loading || validationStatus === 'error'"
              class="mt-4 w-full min-h-[48px] bg-primary hover:bg-primary/50 hover:text-gray-300 px-4 py-2 rounded-[50px] font-bold text-white text-lg disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2">
              <span>{{ loading ? 'Загрузка...' : 'Симулировать' }}</span>
            </button>
          </div>

          <div class="space-y-4 order-last lg:order-none">
            <div class="bg-black/50 rounded-xl p-4 sm:p-5">
              <h3 class="text-lg sm:text-xl font-bold mb-3">Примеры</h3>
              <div class="space-y-2 text-sm mb-[50px]">
                <button @click="loadExample('ethanol')" class="block w-full text-left px-3 py-2 bg-gray-800 rounded-[25px] hover:bg-gray-700 transition min-h-[40px]">Этанол</button>
                <button @click="loadExample('aspirin')" class="block w-full text-left px-3 py-2 bg-gray-800 rounded-[25px] hover:bg-gray-700 transition min-h-[40px]">Аспирин</button>
                <button @click="loadExample('phenobarbital')" class="block w-full text-left px-3 py-2 bg-gray-800 rounded-[25px] hover:bg-gray-700 transition min-h-[40px]">Фенобарбитал</button>
                <button @click="loadExample('fluoxetine')" class="block w-full text-left px-3 py-2 bg-gray-800 rounded-[25px] hover:bg-gray-700 transition min-h-[40px]">Флуоксетин</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>

    <AppFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

interface Atom { id: number; x: number; y: number; symbol: string }
interface Bond { id: number; from: number; to: number; type: 'single' | 'double' | 'triple' }
interface BondLine { x1: number; y1: number; x2: number; y2: number }

const atoms = ref<Atom[]>([])
const bonds = ref<Bond[]>([])
const selectedAtom = ref('C')
const selectedBondType = ref<'single' | 'double' | 'triple'>('single')
const selectedAtomIds = ref<number[]>([])
const selectedBondId = ref<number | null>(null)
const smiles = ref('')
const loading = ref(false)
const validationMsg = ref('')
const validationStatus = ref<'success' | 'warning' | 'error' | null>(null)

const canvasRef = ref<HTMLElement | null>(null)
const isSelecting = ref(false)
const selectStart = ref<{x:number,y:number}|null>(null)
const selectCurrent = ref<{x:number,y:number}|null>(null)
const dragStartPos = ref<{x:number,y:number}|null>(null)
const dragOffsets = ref<Map<number, {dx:number, dy:number}>>(new Map())

let mouseDownPos = { x: 0, y: 0 }
let hasMoved = false
let nextAtomId = 0, nextBondId = 0

const router = useRouter()
const atomList = ['C','O','N','S','Cl','F','P','K','Ca','Na','Mg','Fe','Br','I']

const atomColors: Record<string, {bg:string}> = {
  C:{bg:'#475569'}, O:{bg:'#dc2626'}, N:{bg:'#2563eb'}, S:{bg:'#ca8a04'},
  Cl:{bg:'#16a34a'}, F:{bg:'#0891b2'}, P:{bg:'#9333ea'}, K:{bg:'#8b5cf6'},
  Ca:{bg:'#ec4899'}, Na:{bg:'#f59e0b'}, Mg:{bg:'#14b8a6'}, Fe:{bg:'#ef4444'},
  Br:{bg:'#6366f1'}, I:{bg:'#a855f7'},
  c:{bg:'#475569'}, n:{bg:'#2563eb'}, o:{bg:'#dc2626'}, s:{bg:'#ca8a04'}
}
const maxValency: Record<string, number> = { C:4, O:2, N:3, S:6, Cl:1, F:1, P:5, K:1, Ca:2, Na:1, Mg:2, Fe:3, Br:1, I:1, c:4, n:3, o:2, s:2 }

const selectRect = computed(() => {
  if (!isSelecting.value || !selectStart.value || !selectCurrent.value) return null
  const x = Math.min(selectStart.value.x, selectCurrent.value.x)
  const y = Math.min(selectStart.value.y, selectCurrent.value.y)
  const w = Math.abs(selectCurrent.value.x - selectStart.value.x)
  const h = Math.abs(selectCurrent.value.y - selectStart.value.y)
  return w > 2 && h > 2 ? { x, y, w, h } : null
})

const bondsDisplay = computed(() => bonds.value.map(b => {
  const from = atoms.value.find(a => a.id === b.from)
  const to = atoms.value.find(a => a.id === b.to)
  if (!from || !to) return null
  
  const dx = to.x - from.x, dy = to.y - from.y
  const len = Math.sqrt(dx*dx + dy*dy) || 1
  const nx = -dy/len * 5, ny = dx/len * 5
  
  let lines: BondLine[] = []
  if (b.type === 'single') lines = [{x1:from.x, y1:from.y, x2:to.x, y2:to.y}]
  else if (b.type === 'double') lines = [
    {x1:from.x+nx, y1:from.y+ny, x2:to.x+nx, y2:to.y+ny},
    {x1:from.x-nx, y1:from.y-ny, x2:to.x-nx, y2:to.y-ny}
  ]
  else lines = [
    {x1:from.x, y1:from.y, x2:to.x, y2:to.y},
    {x1:from.x+nx, y1:from.y+ny, x2:to.x+nx, y2:to.y+ny},
    {x1:from.x-nx, y1:from.y-ny, x2:to.x-nx, y2:to.y-ny}
  ]
  return { ...b, lines, isSelected: selectedBondId.value === b.id }
}).filter(Boolean) as Array<Bond & { lines: BondLine[]; isSelected: boolean }>)

const getCoords = (e: MouseEvent | TouchEvent) => {
  const svg = canvasRef.value?.querySelector('svg')
  if (!svg) return { x: 400, y: 200 }
  const rect = svg.getBoundingClientRect()
  const c = 'touches' in e ? (e.touches[0] || e.changedTouches[0]) : e
  return {
    x: Math.max(0, Math.min(800, ((c.clientX - rect.left) / rect.width) * 800)),
    y: Math.max(0, Math.min(400, ((c.clientY - rect.top) / rect.height) * 400))
  }
}

const pointInRect = (px:number, py:number, r:{x:number,y:number,w:number,h:number}) => 
  px >= r.x && px <= r.x + r.w && py >= r.y && py <= r.y + r.h

const distToSeg = (px:number, py:number, x1:number, y1:number, x2:number, y2:number) => {
  const A = px - x1, B = py - y1, C = x2 - x1, D = y2 - y1
  const dot = A * C + B * D, len_sq = C * C + D * D
  const param = len_sq !== 0 ? Math.max(0, Math.min(1, dot / len_sq)) : -1
  return Math.hypot(px - (x1 + param * C), py - (y1 + param * D))
}

const findAtomNear = (c:{x:number,y:number}) => atoms.value.find(a => Math.hypot(a.x - c.x, a.y - c.y) < 22)
const findBondNear = (c:{x:number,y:number}) => bonds.value.find(b => {
  const f = atoms.value.find(a => a.id === b.from)
  const t = atoms.value.find(a => a.id === b.to)
  return f && t && distToSeg(c.x, c.y, f.x, f.y, t.x, t.y) < 12
})

const handleStart = (e: MouseEvent | TouchEvent) => {
  const c = getCoords(e)
  mouseDownPos = { ...c }
  hasMoved = false
  dragStartPos.value = c
  dragOffsets.value.clear()

  const hitAtom = findAtomNear(c)
  const hitBond = !hitAtom ? findBondNear(c) : null

  if (hitAtom) {
    if (e instanceof MouseEvent && e.shiftKey) { removeAtomById(hitAtom.id); return }
    
    if (selectedAtomIds.value.length === 1 && selectedAtomIds.value[0] !== hitAtom.id) {
      addBond(selectedAtomIds.value[0], hitAtom.id, selectedBondType.value)
      selectedAtomIds.value = [hitAtom.id]
    } else {
      selectedAtomIds.value = [hitAtom.id]
      selectedBondId.value = null
    }

    selectedAtomIds.value.forEach(id => {
      const a = atoms.value.find(x => x.id === id)
      if (a) dragOffsets.value.set(id, { dx: a.x - c.x, dy: a.y - c.y })
    })
  } else if (hitBond) {
    if (e instanceof MouseEvent && e.shiftKey) { removeBondById(hitBond.id); return }
    selectedBondId.value = hitBond.id
    selectedAtomIds.value = []
  } else {
    selectedBondId.value = null
    selectedAtomIds.value = []
    isSelecting.value = true
    selectStart.value = c
    selectCurrent.value = c
  }
}

const handleMove = (e: MouseEvent | TouchEvent) => {
  const c = getCoords(e)
  if (!hasMoved) hasMoved = Math.hypot(c.x - mouseDownPos.x, c.y - mouseDownPos.y) > 8

  if (hasMoved && dragStartPos.value && selectedAtomIds.value.length > 0) {
    selectedAtomIds.value.forEach(id => {
      const a = atoms.value.find(x => x.id === id)
      const off = dragOffsets.value.get(id)
      if (a && off) {
        a.x = Math.max(20, Math.min(780, c.x + off.dx))
        a.y = Math.max(20, Math.min(380, c.y + off.dy))
      }
    })
  } else if (isSelecting.value) {
    selectCurrent.value = c
  }
}

const handleEnd = (e: MouseEvent | TouchEvent) => {
  if (e.type === 'mouseleave') { resetInteraction(); return }
  
  const c = getCoords(e)
  
  if (!hasMoved) {
    const hitAtom = findAtomNear(c)
    const hitBond = !hitAtom ? findBondNear(c) : null

    if (hitBond) {
      const order: ('single'|'double'|'triple')[] = ['single', 'double', 'triple']
      const idx = order.indexOf(hitBond.type)
      hitBond.type = order[(idx + 1) % 3]
      selectedBondId.value = hitBond.id
      updateSmiles()
    } else if (!hitAtom) {
      addAtom(c.x, c.y, selectedAtom.value)
      selectedAtomIds.value = []
    }
  } else if (isSelecting.value && selectRect.value) {
    selectedAtomIds.value = atoms.value.filter(a => pointInRect(a.x, a.y, selectRect.value)).map(a => a.id)
  }
  
  resetInteraction()
}

const handleLeave = () => resetInteraction()

const resetInteraction = () => {
  isSelecting.value = false
  dragStartPos.value = null
  hasMoved = false
  selectStart.value = null
  selectCurrent.value = null
}

const addAtom = (x: number, y: number, s: string) => {
  if (atoms.value.some(a => Math.hypot(a.x - x, a.y - y) < 28)) {
    status('warning', 'Атом слишком близко к другому')
    return
  }
  atoms.value.push({ id: nextAtomId++, x, y, symbol: s })
  status('success', `Добавлен ${s}`)
  updateSmiles()
}

const removeAtomById = (id: number) => {
  bonds.value = bonds.value.filter(b => b.from !== id && b.to !== id)
  atoms.value = atoms.value.filter(a => a.id !== id)
  selectedAtomIds.value = selectedAtomIds.value.filter(i => i !== id)
  if (selectedAtomIds.value.length === 0) selectedBondId.value = null
  status('success', 'Удалено')
  updateSmiles()
}

const removeBondById = (id: number) => {
  bonds.value = bonds.value.filter(b => b.id !== id)
  if (selectedBondId.value === id) selectedBondId.value = null
  status('success', 'Связь удалена')
  updateSmiles()
}

const addBond = (f: number, t: number, type: 'single'|'double'|'triple') => {
  if (bonds.value.some(b => (b.from===f && b.to===t) || (b.from===t && b.to===f))) {
    status('error', 'Связь уже существует между этими атомами')
    return
  }
  bonds.value.push({ id: nextBondId++, from: f, to: t, type })
  updateSmiles()
}

const addCycle = (n: number, aromatic = false) => {
  let cx = 400, cy = 200
  if (atoms.value.length > 0) {
    const avgX = atoms.value.reduce((s, a) => s + a.x, 0) / atoms.value.length
    const avgY = atoms.value.reduce((s, a) => s + a.y, 0) / atoms.value.length
    cx = (avgX + 180) % 700 + 50
    cy = (avgY + 100) % 300 + 50
  }

  const radius = 55
  const angleStep = (2 * Math.PI) / n
  const symbol = aromatic ? 'c' : 'C'
  
  const atomIds: number[] = []
  for (let i = 0; i < n; i++) {
    const angle = -Math.PI/2 + i * angleStep
    const x = cx + radius * Math.cos(angle)
    const y = cy + radius * Math.sin(angle)
    const id = nextAtomId++
    atoms.value.push({ id, x, y, symbol })
    atomIds.push(id)
  }
  
  for (let i = 0; i < n; i++) {
    const from = atomIds[i]
    const to = atomIds[(i + 1) % n]
    const type: 'single'|'double' = aromatic && i % 2 === 0 ? 'double' : 'single'
    bonds.value.push({ id: nextBondId++, from, to, type })
  }
  
  updateSmiles()
  status('success', `Добавлен цикл из ${n} атомов`)
}

const clearCanvas = () => {
  atoms.value = []; bonds.value = []; nextAtomId = 0; nextBondId = 0
  selectedAtomIds.value = []; selectedBondId.value = null
  smiles.value = ''; validationMsg.value = ''; validationStatus.value = null
}

const status = (t: 'success'|'warning'|'error', m: string) => {
  validationMsg.value = m; validationStatus.value = t
}



const updateSmiles = () => {
  if (atoms.value.length === 0) { 
    smiles.value = ''; 
    status('error', 'Молекула пуста'); 
    return 
  }
  
  
  const adj = new Map<number, { neighborId: number, bondType: string, bondId: number }[]>()
  atoms.value.forEach(a => adj.set(a.id, []))
  bonds.value.forEach(b => {
    adj.get(b.from)?.push({ neighborId: b.to, bondType: b.type, bondId: b.id })
    adj.get(b.to)?.push({ neighborId: b.from, bondType: b.type, bondId: b.id })
  })

  const visitedAtoms = new Set<number>()
  const visitedBonds = new Set<number>()
  const ringLabels = new Map<number, number>() 
  let currentLabel = 0
  
  
  const dfs = (atomId: number, parentAtomId: number | null): string => {
    visitedAtoms.add(atomId)
    const atom = atoms.value.find(a => a.id === atomId)
    let res = atom?.symbol || '?'
    
    const neighbors = adj.get(atomId) || []
    
    const branches: string[] = []
    
    for (const edge of neighbors) {
      if (visitedBonds.has(edge.bondId)) continue
      
      visitedBonds.add(edge.bondId)
      
      
      if (!visitedAtoms.has(edge.neighborId)) {
        let bondPrefix = ''
        if (edge.bondType === 'double') bondPrefix = '='
        if (edge.bondType === 'triple') bondPrefix = '#'
        
        const subStructure = dfs(edge.neighborId, atomId)
        branches.push(bondPrefix + subStructure)
      } 
      
      else {
        
        if (!ringLabels.has(edge.neighborId)) {
          currentLabel++
          ringLabels.set(edge.neighborId, currentLabel)
        }
        const label = ringLabels.get(edge.neighborId)!
        const labelStr = label > 9 ? `%${label}` : `${label}`
        
        let bondPrefix = ''
        if (edge.bondType === 'double') bondPrefix = '='
        if (edge.bondType === 'triple') bondPrefix = '#'
        
        
        res += bondPrefix + labelStr
      }
    }
    
    
    if (ringLabels.has(atomId)) {
      const label = ringLabels.get(atomId)!
      const labelStr = label > 9 ? `%${label}` : `${label}`
      res += labelStr
    }

    
    res += branches.join('')
    
    return res
  }
  
  
  smiles.value = dfs(atoms.value[0].id, null)
  
  validateMolecule(smiles.value)
}

const validateMolecule = (smi: string) => {
  if (!smi) return status('error', 'Пустая строка')
  if (!/^[A-Za-z0-9\(\)=\#\@\+\-\[\]\\\%\$\.\:\,]+$/.test(smi)) return status('error', 'Недопустимые символы')
  const o = (smi.match(/\(/g)||[]).length, c = (smi.match(/\)/g)||[]).length
  if (o !== c) return status('error', 'Несбалансированные скобки')
  
  const counts = new Map<number, number>()
  atoms.value.forEach(a => counts.set(a.id, 0))
  bonds.value.forEach(b => {
    const m = b.type === 'double' ? 2 : b.type === 'triple' ? 3 : 1
    counts.set(b.from, (counts.get(b.from)||0) + m)
    counts.set(b.to, (counts.get(b.to)||0) + m)
  })
  for (const a of atoms.value) {
    const max = maxValency[a.symbol] || 4, cur = counts.get(a.id) || 0
    if (cur > max) return status('error', `Превышена валентность ${a.symbol} (${cur}/${max})`)
  }
  status('success', 'Структура корректна')
}

const loadExample = (name: string) => {
  clearCanvas()
  type ExAtom = {x:number; y:number; s:string}
  type ExBond = {f:number; t:number; type:'single'|'double'|'triple'}
  
  
  const examples: Record<string, {atoms: ExAtom[]; bonds: ExBond[]}> = {
    ethanol: {
      atoms: [{x:200,y:200,s:'C'}, {x:300,y:200,s:'C'}, {x:400,y:200,s:'O'}],
      bonds: [{f:0,t:1,type:'single'}, {f:1,t:2,type:'single'}]
    },
    aspirin: {
      
      atoms: [
        {x:150,y:200,s:'C'}, 
        {x:210,y:200,s:'C'}, 
        {x:210,y:140,s:'O'}, 
        {x:270,y:200,s:'O'}, 
        {x:330,y:200,s:'c'}, 
        {x:390,y:170,s:'c'}, 
        {x:450,y:200,s:'c'}, 
        {x:450,y:260,s:'c'}, 
        {x:390,y:290,s:'c'}, 
        {x:330,y:260,s:'c'}, 
        {x:510,y:200,s:'C'}, 
        {x:510,y:140,s:'O'}, 
        {x:570,y:200,s:'O'}  
      ],
      bonds: [
        {f:0,t:1,type:'single'}, 
        {f:1,t:2,type:'double'}, 
        {f:1,t:3,type:'single'}, 
        {f:3,t:4,type:'single'}, 
        {f:4,t:5,type:'double'}, 
        {f:5,t:6,type:'single'},
        {f:6,t:7,type:'double'},
        {f:7,t:8,type:'single'},
        {f:8,t:9,type:'double'},
        {f:9,t:4,type:'single'}, 
        {f:6,t:10,type:'single'}, 
        {f:10,t:11,type:'double'}, 
        {f:10,t:12,type:'single'}  
      ]
    },
    phenobarbital: {
      
      atoms: [
        {x:100,y:200,s:'C'}, 
        {x:160,y:200,s:'C'}, 
        {x:220,y:200,s:'C'}, 
        
        
        {x:220,y:260,s:'C'}, 
        {x:280,y:290,s:'N'}, 
        {x:340,y:260,s:'C'}, 
        {x:340,y:200,s:'N'}, 
        {x:280,y:170,s:'C'}, 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        {x:220,y:200,s:'C'}, 
        {x:280,y:170,s:'C'}, 
        {x:340,y:200,s:'N'}, 
        {x:340,y:260,s:'C'}, 
        {x:280,y:290,s:'N'}, 
        {x:220,y:260,s:'C'}, 
        
        
        
        
        
        
        
        
        
        
        
        
        
        {x:100,y:200,s:'C'}, 
        {x:150,y:200,s:'C'}, 
        {x:200,y:200,s:'C'}, 
        
        {x:200,y:260,s:'C'}, 
        {x:250,y:290,s:'N'}, 
        {x:310,y:260,s:'C'}, 
        {x:310,y:200,s:'N'}, 
        {x:250,y:170,s:'C'}, 
        
        
        
        
        {x:200,y:260,s:'C'}, 
        {x:250,y:290,s:'N'}, 
        {x:310,y:260,s:'C'}, 
        {x:310,y:200,s:'N'}, 
        {x:250,y:170,s:'C'}, 
        
        
        {x:200,y:140,s:'c'}, 
        {x:250,y:110,s:'c'}, 
        {x:310,y:140,s:'c'}, 
        {x:310,y:200,s:'c'}, 
        {x:250,y:170,s:'c'}, 
        {x:190,y:170,s:'c'}  
      ],
      bonds: [
        {f:0,t:1,type:'single'},
        {f:1,t:2,type:'single'},
        
        
        {f:2,t:3,type:'single'},
        {f:3,t:4,type:'single'},
        {f:4,t:5,type:'single'},
        {f:5,t:6,type:'single'},
        {f:6,t:7,type:'single'},
        {f:7,t:2,type:'single'},
        
        
        {f:3,t:14,type:'double'}, 
        
      ]
      
      
    },
    fluoxetine: {
      
      atoms: [
        {x:100,y:200,s:'C'}, 
        {x:150,y:200,s:'N'}, 
        {x:200,y:200,s:'C'}, 
        {x:250,y:200,s:'C'}, 
        {x:300,y:200,s:'C'}, 
        
        
        {x:300,y:140,s:'c'}, 
        {x:350,y:110,s:'c'}, 
        {x:400,y:140,s:'c'}, 
        {x:400,y:200,s:'c'}, 
        {x:350,y:230,s:'c'}, 
        {x:300,y:200,s:'c'}, 
        
        
        {x:300,y:140,s:'c'}, 
        {x:350,y:110,s:'c'}, 
        {x:400,y:140,s:'c'}, 
        {x:400,y:200,s:'c'}, 
        {x:350,y:230,s:'c'}, 
        {x:300,y:200,s:'c'}, 
        
        
        {x:350,y:260,s:'O'}, 
        
        
        
        
        {x:400,y:260,s:'c'}, 
        {x:450,y:230,s:'c'}, 
        {x:500,y:260,s:'c'}, 
        {x:500,y:320,s:'c'}, 
        {x:450,y:350,s:'c'}, 
        {x:400,y:320,s:'c'}, 
        
        
        {x:550,y:260,s:'C'}, 
        {x:550,y:200,s:'F'}, 
        {x:600,y:260,s:'F'}, 
        {x:550,y:320,s:'F'}  
      ],
      bonds: [
        {f:0,t:1,type:'single'},
        {f:1,t:2,type:'single'},
        {f:2,t:3,type:'single'},
        {f:3,t:4,type:'single'},
        
        
        {f:4,t:5,type:'single'},
        {f:5,t:6,type:'double'},
        {f:6,t:7,type:'single'},
        {f:7,t:8,type:'double'},
        {f:8,t:9,type:'single'},
        {f:9,t:10,type:'double'},
        {f:10,t:5,type:'single'}, 
        
        
        
        {f:10,t:5,type:'single'}, 

        
        {f:4,t:11,type:'single'},
        {f:11,t:12,type:'single'},
        
        
        {f:12,t:13,type:'double'},
        {f:13,t:14,type:'single'},
        {f:14,t:15,type:'double'},
        {f:15,t:16,type:'single'},
        {f:16,t:17,type:'double'},
        {f:17,t:12,type:'single'},
        
        
        {f:14,t:18,type:'single'},
        {f:18,t:19,type:'single'},
        {f:18,t:20,type:'single'},
        {f:18,t:21,type:'single'}
      ]
    }
  }
  
  
  
  if (name === 'phenobarbital') {
     
     
     
     examples.phenobarbital = {
       atoms: [
         {x:100,y:200,s:'C'}, {x:150,y:200,s:'C'}, {x:200,y:200,s:'C'}, 
         {x:200,y:260,s:'C'}, {x:250,y:290,s:'N'}, {x:310,y:260,s:'C'}, {x:310,y:200,s:'N'}, {x:250,y:170,s:'C'}, 
         {x:200,y:320,s:'O'}, {x:310,y:320,s:'O'}, {x:250,y:110,s:'O'}, 
         {x:200,y:140,s:'c'}, {x:250,y:110,s:'c'}, {x:310,y:140,s:'c'}, {x:310,y:200,s:'c'}, {x:250,y:230,s:'c'}, {x:190,y:200,s:'c'} 
       ],
       bonds: [
         {f:0,t:1,type:'single'}, {f:1,t:2,type:'single'},
         {f:2,t:3,type:'single'}, {f:3,t:4,type:'single'}, {f:4,t:5,type:'single'},
         {f:5,t:6,type:'single'}, {f:6,t:7,type:'single'}, {f:7,t:2,type:'single'},
         {f:3,t:8,type:'double'}, {f:5,t:9,type:'double'}, {f:7,t:10,type:'double'},
         {f:2,t:11,type:'single'}, {f:11,t:12,type:'double'}, {f:12,t:13,type:'single'},
         {f:13,t:14,type:'double'}, {f:14,t:15,type:'single'}, {f:15,t:16,type:'double'},
         {f:16,t:11,type:'single'}
       ]
     }
  }

  const ex = examples[name]
  if (!ex) return
  
  const idMap = new Map<number, number>()
  ex.atoms.forEach((a, idx) => {
    const newId = nextAtomId++
    idMap.set(idx, newId)
    atoms.value.push({ id: newId, x: a.x, y: a.y, symbol: a.s })
  })
  
  ex.bonds.forEach(b => {
    const fromId = idMap.get(b.f)
    const toId = idMap.get(b.t)
    if (fromId !== undefined && toId !== undefined) {
      bonds.value.push({ id: nextBondId++, from: fromId, to: toId, type: b.type })
    }
  })
  
  updateSmiles()
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Delete' || e.key === 'Backspace') {
    e.preventDefault()
    if (selectedAtomIds.value.length > 0) {
      selectedAtomIds.value.forEach(id => removeAtomById(id))
    } else if (selectedBondId.value !== null) {
      removeBondById(selectedBondId.value)
    }
  }
}

const simulate = async () => {
  if (validationStatus.value !== 'success') return
  loading.value = true
  try {
    const res = await $fetch('/api/predict/biotargets', { method: 'POST', body: { smiles: smiles.value } })
    localStorage.setItem('lastSmiles', smiles.value) 
    localStorage.setItem('lastPrediction', JSON.stringify(res))
    router.push('/result')
  } catch (e: any) {
    status('error', e.message || 'Ошибка сервера')
  } finally { loading.value = false }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
  loadExample('ethanol')
})
onUnmounted(() => window.removeEventListener('keydown', handleKeyDown))
</script>
