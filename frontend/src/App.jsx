import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Scatter, ScatterChart, ZAxis, AreaChart, Area
} from 'recharts';
import { AlertTriangle, ShieldCheck, Activity, TrendingUp, Info, RefreshCw, ChevronRight } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api';

const App = () => {
  const [stocks, setStocks] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState(null);
  const [stockDetail, setStockDetail] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/stocks`);
      setStocks(res.data);
      if (res.data.length > 0 && !selectedTicker) {
        handleSelectTicker(res.data[0].ticker);
      }
    } catch (err) {
      setError("Failed to fetch stocks. Is the backend running?");
    } finally {
      setLoading(false);
    }
  };

  const handleSelectTicker = async (ticker) => {
    setSelectedTicker(ticker);
    try {
      const res = await axios.get(`${API_BASE}/stocks/${ticker}`);
      setStockDetail(res.data);
    } catch (err) {
      console.error("Error fetching stock detail", err);
    }
  };

  const getRiskColor = (score) => {
    if (score < 30) return 'text-green-400 border-green-900/50 bg-green-900/10';
    if (score < 70) return 'text-yellow-400 border-yellow-900/50 bg-yellow-900/10';
    return 'text-red-400 border-red-900/50 bg-red-900/10';
  };

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded shadow-xl">
          <p className="text-slate-300 font-bold mb-1">{label}</p>
          <p className="text-blue-400">Price: ₹{payload[0].value.toFixed(2)}</p>
          {payload[0].payload.anomaly && (
            <p className="text-red-400 font-bold flex items-center gap-1">
              <AlertTriangle size={14} /> Anomaly Detected
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans p-6">
      {/* Header */}
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-black tracking-tight text-white flex items-center gap-2">
            <ShieldCheck className="text-blue-500" size={32} />
            STOCK RISK <span className="text-blue-500">AI</span>
          </h1>
          <p className="text-slate-400 text-sm">LSTM Autoencoder-based Anomaly Detection</p>
        </div>
        <button 
          onClick={fetchStocks}
          className="bg-slate-900 hover:bg-slate-800 border border-slate-800 p-2 rounded-full transition-all group"
        >
          <RefreshCw size={20} className={`group-hover:rotate-180 transition-transform duration-500 ${loading ? 'animate-spin' : ''}`} />
        </button>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-12 gap-8">
        
        {/* Left Sidebar: Leaderboard */}
        <div className="col-span-12 lg:col-span-4 space-y-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-xl font-bold">Risk Leaderboard</h2>
            <span className="text-xs text-slate-500 bg-slate-900 px-2 py-1 rounded">NSE Stocks</span>
          </div>
          
          <div className="space-y-3 overflow-y-auto max-h-[calc(100vh-200px)] pr-2 custom-scrollbar">
            {loading && [1,2,3,4].map(i => (
              <div key={i} className="h-20 bg-slate-900/50 animate-pulse rounded-xl border border-slate-800" />
            ))}
            
            {stocks.map((stock) => (
              <div 
                key={stock.ticker}
                onClick={() => handleSelectTicker(stock.ticker)}
                className={`
                  p-4 rounded-xl border cursor-pointer transition-all duration-200 flex items-center justify-between
                  ${selectedTicker === stock.ticker 
                    ? 'border-blue-500 bg-blue-500/5 shadow-[0_0_15px_rgba(59,130,246,0.1)]' 
                    : 'border-slate-800 bg-slate-900/40 hover:border-slate-700'}
                `}
              >
                <div>
                  <h3 className="font-bold text-lg">{stock.ticker.split('.')[0]}</h3>
                  <p className="text-slate-500 text-sm">₹{stock.price.toFixed(2)}</p>
                </div>
                <div className="text-right flex items-center gap-3">
                  <div className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-widest border ${getRiskColor(stock.risk_score)}`}>
                    {stock.risk_score.toFixed(0)}%
                  </div>
                  {stock.is_anomaly && <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]" />}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Content: Analysis */}
        <div className="col-span-12 lg:col-span-8 space-y-6">
          {!stockDetail ? (
            <div className="h-full flex items-center justify-center text-slate-600 border-2 border-dashed border-slate-900 rounded-3xl">
              <p>Select a stock to see deep-dive analysis</p>
            </div>
          ) : (
            <>
              {/* Stats Cards */}
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl">
                  <div className="text-slate-500 text-xs mb-1 flex items-center gap-1 uppercase tracking-wider">
                    <Activity size={14} /> Risk Level
                  </div>
                  <div className={`text-3xl font-black ${stockDetail.current_risk > 70 ? 'text-red-500' : 'text-blue-400'}`}>
                    {stockDetail.current_risk.toFixed(1)}%
                  </div>
                </div>
                <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl">
                  <div className="text-slate-500 text-xs mb-1 flex items-center gap-1 uppercase tracking-wider">
                    <AlertTriangle size={14} /> Status
                  </div>
                  <div className={`text-3xl font-black uppercase ${stockDetail.is_anomaly ? 'text-red-500' : 'text-green-500'}`}>
                    {stockDetail.is_anomaly ? 'Anomalous' : 'Normal'}
                  </div>
                </div>
                <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl">
                  <div className="text-slate-500 text-xs mb-1 flex items-center gap-1 uppercase tracking-wider">
                    <TrendingUp size={14} /> Volatility
                  </div>
                  <div className="text-3xl font-black text-slate-200">
                    {stockDetail.history[stockDetail.history.length-1].volatility.toFixed(3)}
                  </div>
                </div>
              </div>

              {/* Main Chart */}
              <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl">
                <div className="flex justify-between items-center mb-6">
                  <h3 className="text-xl font-bold flex items-center gap-2">
                    Anomaly Inspector <span className="text-xs font-normal text-slate-500 bg-slate-800 px-2 py-0.5 rounded">Historical</span>
                  </h3>
                  <div className="flex gap-4 text-xs">
                    <span className="flex items-center gap-1 text-slate-400"><div className="w-2 h-2 bg-blue-500 rounded-full" /> Price</span>
                    <span className="flex items-center gap-1 text-slate-400"><div className="w-2 h-2 bg-red-500 rounded-full" /> Anomaly</span>
                  </div>
                </div>
                
                <div className="h-80 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={stockDetail.history}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                      <XAxis dataKey="date" stroke="#64748b" fontSize={10} tickMargin={10} axisLine={false} />
                      <YAxis stroke="#64748b" fontSize={10} axisLine={false} tickFormatter={(v) => `₹${v}`} />
                      <Tooltip content={<CustomTooltip />} />
                      <Line 
                        type="monotone" 
                        dataKey="price" 
                        stroke="#3b82f6" 
                        strokeWidth={2} 
                        dot={(props) => {
                          const { cx, cy, payload } = props;
                          if (payload.anomaly) {
                            return <circle cx={cx} cy={cy} r={4} fill="#ef4444" stroke="none" className="animate-pulse" />;
                          }
                          return null;
                        }} 
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Error Grapah */}
              <div className="bg-slate-900/40 border border-slate-800 p-6 rounded-3xl">
                <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-4">Model Reconstruction Error (Signal Intensity)</h3>
                <div className="h-32 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={stockDetail.history}>
                      <Area type="monotone" dataKey="error" stroke="#8b5cf6" fill="#8b5cf61a" strokeWidth={1} />
                      <Tooltip labelStyle={{color: '#000'}} itemStyle={{fontSize: '12px'}} />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}
        </div>
      </main>

      <footer className="max-w-7xl mx-auto mt-12 pt-8 border-t border-slate-900 text-center text-slate-600 text-xs">
        <p>This is an AI-powered risk assessment tool and does not constitute financial advice. Anomaly detection is based on LSTM reconstruction error.</p>
      </footer>
    </div>
  );
};

export default App;
