import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Droplets, Activity, Brain, Settings, AlertTriangle, CheckCircle, Info, Waves } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const App = () => {
  // --- 1. STATE YÖNETİMİ ---
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [params, setParams] = useState({
    capacity: 5000,
    area: 50,
    current: 4200,
    runoff: 0.9,
    month: 1
  });

  // --- 2. GİRDİ DOĞRULAMA (VALIDATION) ---
  const handleParamChange = (key, rawValue) => {
    let val = parseFloat(rawValue);
    if (isNaN(val)) { setParams(prev => ({ ...prev, [key]: 0 })); return; }

    if (key === 'month') val = Math.max(1, Math.min(12, val));
    else if (key === 'runoff') val = Math.max(0, Math.min(1, val));
    else val = Math.max(0, val);

    setParams(prev => ({ ...prev, [key]: val }));
  };

  // --- 3. API BAĞLANTISI ---
  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`http://127.0.0.1:8000/analyze`, {
        params: {
          capacity: params.capacity,
          area: params.area,
          current: params.current,
          runoff: params.runoff,
          month: params.month
        }
      });
      setData(response.data);
    } catch (error) {
      console.error("API Connection Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (!data) return (
    <div className="flex flex-col items-center justify-center h-screen bg-slate-950 text-blue-400">
      <motion.div animate={{ rotate: 360 }} transition={{ repeat: Infinity, duration: 2 }}>
        <Droplets size={48} />
      </motion.div>
      <p className="mt-4 font-mono tracking-widest animate-pulse">CONNECTING TO DIGITAL TWIN...</p>
    </div>
  );

  // --- 4. HESAPLAMALAR VE TEMALANDIRMA ---
  const fillPercent = Math.min(100, (data.tank.predicted_level / data.tank.capacity) * 100);

  const getStatusTheme = (status) => {
    switch (status) {
      case 'CRITICAL_OVERFLOW':
        return { color: 'text-red-400', bg: 'bg-red-500/10', border: 'border-red-500/50', icon: <AlertTriangle /> };
      case 'CRITICAL_LOW':
        return { color: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/50', icon: <AlertTriangle /> };
      default:
        return { color: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/50', icon: <CheckCircle /> };
    }
  };

  const theme = getStatusTheme(data.tank.status_code);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-4 md:p-8 font-sans selection:bg-blue-500/30">

      {/* HEADER */}
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-10 border-b border-slate-900 pb-6">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2.5 rounded-2xl shadow-lg shadow-blue-500/20">
            <Droplets size={28} className="text-white" />
          </div>
          <div>
            <h1 className="text-xl font-black tracking-tighter">WATERTWIN <span className="text-blue-500">PRO</span></h1>
            <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest">Smart Management System</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="hidden md:flex flex-col items-end">
            <span className="text-[10px] font-bold text-slate-500 uppercase">System Status</span>
            <span className="text-xs font-mono text-emerald-500 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping" /> ONLINE
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8">

        {/* CONTROLS */}
        <aside className="lg:col-span-3 space-y-6">
          <div className="bg-slate-900/40 p-6 rounded-[2rem] border border-slate-800 backdrop-blur-md shadow-xl">
            <h3 className="flex items-center gap-2 font-bold mb-6 text-slate-300 text-sm uppercase tracking-wider">
              <Settings size={16} className="text-blue-500" /> Control Panel
            </h3>

            <div className="space-y-5">
              {[
                { label: 'Tank Capacity (L)', key: 'capacity', step: 100, min: 0 },
                { label: 'Roof Area (m²)', key: 'area', step: 1, min: 0 },
                { label: 'Current Level (L)', key: 'current', step: 10, min: 0 },
                { label: 'Runoff Coeff (0-1)', key: 'runoff', step: 0.05, min: 0, max: 1 },
                { label: 'Simulation Month (1-12)', key: 'month', step: 1, min: 1, max: 12 }
              ].map((input) => (
                <div key={input.key} className="group">
                  <label className="text-[10px] text-slate-500 uppercase font-black mb-1.5 block group-focus-within:text-blue-400 transition-colors">
                    {input.label}
                  </label>
                  <input
                    type="number"
                    step={input.step}
                    min={input.min}
                    max={input.max}
                    value={params[input.key]}
                    onChange={(e) => handleParamChange(input.key, e.target.value)}
                    className="w-full bg-slate-800/40 border border-slate-700/50 rounded-xl px-4 py-3 focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 outline-none transition-all font-mono text-sm"
                  />
                </div>
              ))}

              <button
                onClick={fetchData}
                disabled={loading}
                className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-slate-800 text-white py-4 rounded-2xl font-black text-xs uppercase tracking-widest transition-all shadow-lg shadow-blue-600/20 active:scale-[0.98]"
              >
                {loading ? 'Processing...' : 'Sync Digital Twin'}
              </button>
            </div>
          </div>

          <div className="bg-slate-900/40 p-6 rounded-[2rem] border border-slate-800">
            <h3 className="flex items-center gap-2 font-bold mb-4 text-slate-400 text-[10px] uppercase tracking-widest">
              <Activity size={14} /> AI Model Metrics
            </h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-950/50 p-3 rounded-2xl border border-slate-800/50">
                <p className="text-[9px] text-slate-600 uppercase font-bold">Accuracy</p>
                <p className="text-md font-black text-blue-500">{data.weather.metrics.Accuracy}</p>
              </div>
              <div className="bg-slate-950/50 p-3 rounded-2xl border border-slate-800/50">
                <p className="text-[9px] text-slate-600 uppercase font-bold">R2 Score</p>
                <p className="text-md font-black text-blue-500">{data.weather.metrics.R2}</p>
              </div>
            </div>
          </div>
        </aside>

        {/* TANK VISUALIZATION */}
        <section className="lg:col-span-6">
          <div className="bg-slate-900/20 p-8 rounded-[3rem] border border-slate-800/50 flex flex-col items-center justify-center relative min-h-[600px] shadow-2xl overflow-hidden">

            <div className="absolute top-8 left-1/2 -translate-x-1/2 text-center">
              <h2 className="text-sm font-black uppercase tracking-[0.3em] text-slate-600">Simulated Storage</h2>
            </div>

            {/* ANA TANK GÖVDESİ */}
            <div className="relative w-64 h-80 bg-slate-950/50 rounded-b-[3rem] rounded-t-2xl border-[6px] border-slate-800 shadow-2xl backdrop-blur-sm mt-8 overflow-hidden">

              {/* SU SEVİYESİ */}
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: `${fillPercent}%` }}
                transition={{ duration: 2, ease: "circOut" }}
                className={`absolute bottom-0 w-full ${fillPercent >= 100 ? 'bg-red-500/40' : 'bg-blue-500/40'} rounded-b-[2.4rem] overflow-hidden z-0`}
              >
                <div className="absolute top-0 left-0 w-full h-4 bg-white/20 blur-sm animate-pulse" />
                <Waves className="absolute -top-6 left-0 w-[200%] h-12 text-blue-400/20 animate-[wave_3s_infinite_linear]" />
              </motion.div>

              {/* YÜZDE GÖSTERGESİ */}
              <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none z-10">
                <span className="text-6xl font-black font-mono text-white drop-shadow-2xl">
                  {Math.round(fillPercent)}%
                </span>
                <span className={`text-[10px] uppercase font-black px-2 py-0.5 rounded mt-2 ${theme.bg} ${theme.color}`}>
                  {data.tank.status_code.replace('_', ' ')}
                </span>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-10 mt-16 w-full border-t border-slate-900 pt-10 px-4">
              <div className="text-center group">
                <p className="text-[10px] text-slate-500 uppercase font-black mb-1">Precipitation</p>
                <p className="text-2xl font-black font-mono">{data.weather.rain_forecast_mm}<span className="text-xs ml-1 text-slate-600">mm</span></p>
              </div>
              <div className="text-center group border-x border-slate-900">
                <p className="text-[10px] text-slate-500 uppercase font-black mb-1">Total Incoming</p>
                <p className="text-2xl font-black font-mono text-blue-500">+{Math.round(data.tank.incoming_water)}<span className="text-xs ml-1 text-slate-600">L</span></p>
              </div>
              <div className="text-center group">
                <p className="text-[10px] text-slate-500 uppercase font-black mb-1">New Total</p>
                <p className="text-2xl font-black font-mono text-emerald-500">{Math.round(data.tank.predicted_level)}<span className="text-xs ml-1 text-slate-600">L</span></p>
              </div>
            </div>
          </div>
        </section>

        {/* AI & ALERTS */}
        <section className="lg:col-span-3 space-y-6">
          <AnimatePresence mode="wait">
            <motion.div
              key={data.tank.status_code}
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              className={`p-6 rounded-[2.5rem] flex items-center gap-4 border-2 ${theme.bg} ${theme.border} ${theme.color} shadow-2xl`}
            >
              <div className="bg-slate-950 p-3 rounded-2xl shadow-inner">
                {theme.icon}
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] font-black uppercase tracking-tighter opacity-70 italic">System Alert</span>
                <span className="text-sm font-black uppercase leading-tight">{data.tank.status_code.replace('_', ' ')}</span>
              </div>
            </motion.div>
          </AnimatePresence>

          <div className="bg-gradient-to-br from-blue-600 to-indigo-800 p-8 rounded-[3rem] shadow-2xl relative overflow-hidden group border border-white/10">
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:scale-150 transition-transform duration-1000">
              <Brain size={120} />
            </div>

            <h3 className="font-black flex items-center gap-2 mb-6 text-white uppercase text-[10px] tracking-[0.2em]">
              <Brain size={18} /> AI Decision Support
            </h3>

            <div className="relative z-10">
              <p className="text-sm leading-relaxed text-blue-50 font-bold italic tracking-wide">
                "{data.ai_assistant.message}"
              </p>
              <div className="mt-8 pt-6 border-t border-white/10 flex items-center gap-2">
                <div className="w-2 h-2 bg-blue-300 rounded-full animate-pulse" />
                <span className="text-[9px] font-black text-blue-200 uppercase tracking-widest">Powered by WaterTwin LLM Core</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900/40 p-6 rounded-[2rem] border border-slate-800">
            <div className="flex items-start gap-3">
              <Info className="text-slate-500 mt-1" size={16} />
              <p className="text-[11px] text-slate-400 font-medium leading-relaxed">
                <span className="text-slate-200 font-bold">Pro Tip:</span> Adjusting the <span className="text-blue-400">Runoff Coefficient</span> based on your roof material ensures simulation accuracy.
              </p>
            </div>
          </div>
        </section>
      </main>

      <footer className="max-w-7xl mx-auto mt-16 text-center border-t border-slate-900 pt-8">
        <p className="text-[9px] font-black text-slate-700 uppercase tracking-[0.5em]">
          Hydro-Twin Predictive Simulation Engine • 2024 Final Project
        </p>
      </footer>
    </div>
  );
};

export default App;