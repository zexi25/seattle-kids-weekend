// src/components/FilterBar.tsx
'use client';

import React from 'react';
import { 
  Search, 
  Leaf, 
  Music, 
  Sparkles, 
  Compass, 
  Home, 
  Check, 
  Ticket 
} from 'lucide-react';

export type DatePreset = 'month_and_next' | 'this_weekend' | 'next_weekend' | 'custom';
export type RegionKey = 'seattle' | 'eastside' | 'north' | 'south';
export type AgeBucket = 'preschool' | 'elementary';
export type TimeSlot = 'morning' | 'afternoon';
export type CategoryKey = 'all' | 'nature_animals' | 'music_crafts' | 'festivals_markets' | 'exploration_exp';

export interface FilterState {
  datePreset: DatePreset;
  searchQuery: string;
  regions: RegionKey[];
  ageBuckets: AgeBucket[];
  timeSlots: TimeSlot[];
  isFreeOnly: boolean;
  isIndoorOnly: boolean;
  category: CategoryKey;
}

interface FilterBarProps {
  filters: FilterState;
  onChange: (filters: FilterState) => void;
  dateRangeDisplay?: string; // 类似 "11/2–12/31 · 2026"
}

const REGION_OPTIONS: { key: RegionKey; label: string }[] = [
  { key: 'seattle', label: '西雅图市' },
  { key: 'eastside', label: '东区' },
  { key: 'north', label: '北区' },
  { key: 'south', label: '南区' },
];

const AGE_OPTIONS: { key: AgeBucket; label: string }[] = [
  { key: 'preschool', label: '学龄前 · 0–5 岁' },
  { key: 'elementary', label: '小学 · 6–12 岁' },
];

const TIME_OPTIONS: { key: TimeSlot; label: string }[] = [
  { key: 'morning', label: '上午' },
  { key: 'afternoon', label: '下午' },
];

const CATEGORY_TABS: { key: CategoryKey; label: string; icon: React.ReactNode }[] = [
  { key: 'all', label: '全部类型', icon: null },
  { key: 'nature_animals', label: '自然与动物', icon: <Leaf className="w-4 h-4" /> },
  { key: 'music_crafts', label: '音乐与手作', icon: <Music className="w-4 h-4" /> },
  { key: 'festivals_markets', label: '节庆与市集', icon: <Sparkles className="w-4 h-4" /> },
  { key: 'exploration_exp', label: '探索与体验', icon: <Compass className="w-4 h-4" /> },
];

export default function FilterBar({
  filters,
  onChange,
  dateRangeDisplay = '11/2–12/31 · 2026',
}: FilterBarProps) {

  // 数组多选切换辅助函数
  const toggleArrayItem = <T extends string>(list: T[], item: T): T[] => {
    return list.includes(item) ? list.filter((i) => i !== item) : [...list, item];
  };

  return (
    <div className="w-full bg-white border-b border-slate-200 text-slate-700 text-sm select-none">
      <div className="max-w-[1600px] mx-auto px-4 py-2.5 flex flex-col gap-2.5">
        
        {/* 第一行：时间轴预设 + 搜索栏 */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-1.5 flex-wrap">
            <div className="inline-flex rounded-lg bg-slate-100 p-0.5 text-xs font-medium text-slate-600">
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'month_and_next' })}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  filters.datePreset === 'month_and_next'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                本月及下月
              </button>
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'this_weekend' })}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  filters.datePreset === 'this_weekend'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                本周末
              </button>
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'next_weekend' })}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  filters.datePreset === 'next_weekend'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                下周末
              </button>
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'custom' })}
                className={`px-3 py-1.5 rounded-md transition-all ${
                  filters.datePreset === 'custom'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                自选日期
              </button>
            </div>
            
            <span className="text-xs text-slate-400 font-mono ml-2 hidden sm:inline">
              {dateRangeDisplay}
            </span>
          </div>

          {/* 搜索输入框 */}
          <div className="relative min-w-[240px] max-w-xs flex-1 sm:flex-initial">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="活动、城市、场馆"
              value={filters.searchQuery}
              onChange={(e) => onChange({ ...filters, searchQuery: e.target.value })}
              className="w-full bg-slate-100 hover:bg-slate-200/70 focus:bg-white text-xs text-slate-800 pl-9 pr-4 py-1.5 rounded-lg border border-transparent focus:border-slate-300 focus:outline-none transition-all placeholder:text-slate-400"
            />
          </div>
        </div>

        {/* 第二行：细分复选器（地区、年龄、时段、免费与室内开关） */}
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2 text-xs text-slate-600 pt-0.5">
          {/* 地区 */}
          <div className="flex items-center gap-2">
            <span className="text-slate-400">地区</span>
            <div className="flex items-center gap-2">
              {REGION_OPTIONS.map((item) => {
                const checked = filters.regions.includes(item.key);
                return (
                  <label
                    key={item.key}
                    className="flex items-center gap-1 cursor-pointer hover:text-slate-900 select-none"
                  >
                    <span
                      onClick={() =>
                        onChange({
                          ...filters,
                          regions: toggleArrayItem(filters.regions, item.key),
                        })
                      }
                      className={`w-3.5 h-3.5 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white'
                          : 'border-slate-300 bg-white hover:border-slate-400'
                      }`}
                    >
                      {checked && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                    </span>
                    <span>{item.label}</span>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="h-3 w-[1px] bg-slate-200 hidden sm:block" />

          {/* 年龄段 */}
          <div className="flex items-center gap-2">
            <span className="text-slate-400">年龄</span>
            <div className="flex items-center gap-2">
              {AGE_OPTIONS.map((item) => {
                const checked = filters.ageBuckets.includes(item.key);
                return (
                  <label
                    key={item.key}
                    className="flex items-center gap-1 cursor-pointer hover:text-slate-900 select-none"
                  >
                    <span
                      onClick={() =>
                        onChange({
                          ...filters,
                          ageBuckets: toggleArrayItem(filters.ageBuckets, item.key),
                        })
                      }
                      className={`w-3.5 h-3.5 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white'
                          : 'border-slate-300 bg-white hover:border-slate-400'
                      }`}
                    >
                      {checked && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                    </span>
                    <span>{item.label}</span>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="h-3 w-[1px] bg-slate-200 hidden sm:block" />

          {/* 时段 */}
          <div className="flex items-center gap-2">
            <span className="text-slate-400">时段</span>
            <div className="flex items-center gap-2">
              {TIME_OPTIONS.map((item) => {
                const checked = filters.timeSlots.includes(item.key);
                return (
                  <label
                    key={item.key}
                    className="flex items-center gap-1 cursor-pointer hover:text-slate-900 select-none"
                  >
                    <span
                      onClick={() =>
                        onChange({
                          ...filters,
                          timeSlots: toggleArrayItem(filters.timeSlots, item.key),
                        })
                      }
                      className={`w-3.5 h-3.5 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white'
                          : 'border-slate-300 bg-white hover:border-slate-400'
                      }`}
                    >
                      {checked && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                    </span>
                    <span>{item.label}</span>
                  </label>
                );
              })}
            </div>
          </div>

          <div className="h-3 w-[1px] bg-slate-200 hidden md:block" />

          {/* 特性开关：免费入场 + 室内避雨 */}
          <div className="flex items-center gap-3">
            {/* 免费入场 */}
            <label className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 select-none">
              <span
                onClick={() => onChange({ ...filters, isFreeOnly: !filters.isFreeOnly })}
                className={`w-3.5 h-3.5 rounded flex items-center justify-center border transition-colors ${
                  filters.isFreeOnly
                    ? 'bg-slate-900 border-slate-900 text-white'
                    : 'border-slate-300 bg-white hover:border-slate-400'
                }`}
              >
                {filters.isFreeOnly && <Check className="w-2.5 h-2.5 stroke-[3]" />}
              </span>
              <Ticket className="w-3.5 h-3.5 text-slate-500" />
              <span>免费入场</span>
            </label>

            {/* 西雅图刚需：室内避雨 */}
            <label className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 select-none">
              <span
                onClick={() => onChange({ ...filters, isIndoorOnly: !filters.isIndoorOnly })}
                className={`w-3.5 h-3.5 rounded flex items-center justify-center border transition-colors ${
                  filters.isIndoorOnly
                    ? 'bg-slate-900 border-slate-900 text-white'
                    : 'border-slate-300 bg-white hover:border-slate-400'
                }`}
              >
                {filters.isIndoorOnly && <Check className="w-2.5 h-2.5 stroke-[3]" />}
              </span>
              <Home className="w-3.5 h-3.5 text-slate-500" />
              <span>室内避雨</span>
            </label>
          </div>
        </div>

        {/* 第三行：分类胶囊导航 (Pill Tabs) */}
        <div className="flex items-center gap-2 overflow-x-auto pt-1 no-scrollbar">
          {CATEGORY_TABS.map((tab) => {
            const isActive = filters.category === tab.key;
            return (
              <button
                key={tab.key}
                type="button"
                onClick={() => onChange({ ...filters, category: tab.key })}
                className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-full text-xs font-medium shrink-0 transition-all ${
                  isActive
                    ? 'bg-slate-100 text-slate-900 ring-1 ring-slate-300 shadow-inner'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                {tab.icon && (
                  <span className={isActive ? 'text-slate-900' : 'text-slate-500'}>
                    {tab.icon}
                  </span>
                )}
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </div>
  );
}