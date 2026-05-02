'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

// Charts
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts'

export default function Dashboard() {
  const [amount, setAmount] = useState(100)
  const [hour, setHour] = useState(12)
  const [result, setResult] = useState(null)
  const [stats, setStats] = useState(null)
 const [history, setHistory] = useState<any[]>([])
  // Fetch stats
  useEffect(() => {
    fetch('https://credit-card-fraud-detection-system-1-mubd.onrender.com/stats')
      .then(res => res.json())
      .then(data => setStats(data))
  }, [])

  // Chart data
  const fraudTrend = [
    { day: 'Mon', fraud: 20 },
    { day: 'Tue', fraud: 35 },
    { day: 'Wed', fraud: 28 },
    { day: 'Thu', fraud: 50 },
    { day: 'Fri', fraud: 40 },
    { day: 'Sat', fraud: 65 },
    { day: 'Sun', fraud: 45 },
  ]

  const riskDistribution = [
    { name: 'Low Risk', value: 70 },
    { name: 'Medium Risk', value: 20 },
    { name: 'High Risk', value: 10 },
  ]

  // Prediction
  const handlePredict = async () => {
    const payload = {
      V1: -1.35, V2: -0.07, V3: 2.53, V4: 1.37, V5: -0.33,
      V6: 0.46, V7: 0.23, V8: 0.09, V9: 0.36, V10: 0.09,
      V11: -0.55, V12: -0.61, V13: -0.99, V14: -0.31,
      V15: 1.46, V16: -0.47, V17: 0.20, V18: 0.02,
      V19: 0.40, V20: 0.25, V21: -0.01, V22: 0.27,
      V23: -0.11, V24: 0.06, V25: 0.12, V26: -0.18,
      V27: 0.13, V28: -0.02,
      Amount: amount,
      Hour: hour,
      Amount_log: Math.log1p(amount)
    }

    const res = await fetch('https://credit-card-fraud-detection-system-1-mubd.onrender.com/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    })

    const data = await res.json()

    setResult(data)
    setHistory(prev => [data, ...prev.slice(0, 4)])
  }

  return (
    <div className="flex min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white">

      {/* SIDEBAR */}
      <div className="w-60 bg-black/70 border-r border-gray-800 p-6">
        <h2 className="text-xl font-bold text-blue-400 mb-8">FraudAI</h2>

        <div className="flex flex-col space-y-5 text-sm">
          <Link href="/" className="text-blue-400 hover:translate-x-1 transition">Overview</Link>
          <Link href="/transactions" className="opacity-70 hover:text-white hover:translate-x-1 transition">Transactions</Link>
          <Link href="/alerts" className="opacity-70 hover:text-white hover:translate-x-1 transition">Alerts</Link>
          <Link href="/settings" className="opacity-70 hover:text-white hover:translate-x-1 transition">Settings</Link>
        </div>
      </div>

      {/* MAIN */}
      <div className="flex-1 p-8 space-y-8">

        <h1 className="text-2xl font-bold">Fraud Detection Dashboard</h1>

        {/* STATS */}
        <div className="grid grid-cols-3 gap-6">
          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <p className="text-gray-400 text-sm">Transactions</p>
            <h2 className="text-2xl font-bold">
              {stats ? stats.total_transactions : '...'}
            </h2>
          </div>

          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <p className="text-gray-400 text-sm">Frauds Detected</p>
            <h2 className="text-2xl font-bold text-red-400">
              {stats ? stats.fraud_count : '...'}
            </h2>
          </div>

          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <p className="text-gray-400 text-sm">Accuracy</p>
            <h2 className="text-2xl font-bold text-green-400">
              {stats ? `${(stats.accuracy * 100).toFixed(0)}%` : '...'}
            </h2>
          </div>
        </div>

        {/* CHARTS */}
        <div className="grid grid-cols-2 gap-6">

          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <h2 className="mb-4 font-semibold">Fraud Trend</h2>
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={fraudTrend}>
                <XAxis dataKey="day" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip />
                <Line type="monotone" dataKey="fraud" stroke="#3b82f6" strokeWidth={3}/>
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-white/5 p-6 rounded-2xl border border-white/10">
            <h2 className="mb-4 font-semibold">Risk Distribution</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={riskDistribution}>
                <XAxis dataKey="name" stroke="#aaa" />
                <YAxis stroke="#aaa" />
                <Tooltip />
                <Bar dataKey="value" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>

        </div>

        {/* INPUT */}
        <div className="flex justify-center">
          <div className="bg-white/5 p-8 rounded-2xl border border-white/10 w-full max-w-lg space-y-6">

            <h2 className="text-lg font-semibold">Test Transaction</h2>

            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(Number(e.target.value))}
              className="w-full p-3 bg-black/50 border border-gray-700 rounded"
              placeholder="Transaction Amount"
            />

            <input
              type="number"
              value={hour}
              onChange={(e) => setHour(Number(e.target.value))}
              className="w-full p-3 bg-black/50 border border-gray-700 rounded"
              placeholder="Hour (0-23)"
            />

            <button
              onClick={handlePredict}
              className="w-full bg-gradient-to-r from-blue-500 to-indigo-600 p-3 rounded hover:scale-105 transition"
            >
              Analyze Transaction
            </button>

          </div>
        </div>

        {/* RESULT */}
        {result && (
          <div className="flex justify-center">
            <div className="bg-white/5 p-6 rounded-2xl border border-white/10 w-full max-w-lg text-center">
              <p><strong>Fraud Probability:</strong> {result.fraud_probability}</p>
              <p className="mt-2">
                <strong>Status:</strong>{' '}
                <span className={result.decision === 'REVIEW' ? 'text-red-400' : 'text-green-400'}>
                  {result.decision}
                </span>
              </p>
            </div>
          </div>
        )}

        {/* HISTORY */}
        <div className="flex justify-center">
          <div className="bg-white/5 p-6 rounded-2xl border border-white/10 w-full max-w-lg">
            <h2 className="mb-3 font-semibold">Recent Predictions</h2>

            {history.map((item, i) => (
              <div key={i} className="flex justify-between py-1 text-sm">
                <span>{item.fraud_probability}</span>
                <span className={item.decision === 'REVIEW' ? 'text-red-400' : 'text-green-400'}>
                  {item.decision}
                </span>
              </div>
            ))}

          </div>
        </div>

      </div>
    </div>
  )
}