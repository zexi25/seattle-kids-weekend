// src/components/FilterBar.tsx
'use client';

import React, { useState, useEffect } from 'react';
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
  customStartDate?: string;
  customEndDate?: string;
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
  { key: 'nature_animals', label: '自然与动物', icon: <Leaf className="w-3.5 h-3.5" /> },
  { key: 'music_crafts', label: '音乐与手作', icon: <Music className="w-3.5 h-3.5" /> },
  { key: 'festivals_markets', label: '节庆与市集', icon: <Sparkles className="w-3.5 h-3.5" /> },
  { key: 'exploration_exp', label: '探索与体验', icon: <Compass className="w-3.5 h-3.5" /> },
];

export default function FilterBar({
  filters,
  onChange,
}: FilterBarProps) {
  const [dateBounds, setDateBounds] = useState({
    todayStr: '',
    maxLimitStr: '',
    maxDisplayLabel: '',
    defaultRangeText: '',
  });

  useEffect(() => {
    const now = new Date();
    const pad = (n: number) => String(n).padStart(2, '0');
    const toYMD = (d: Date) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;

    const todayStr = toYMD(now);
    const maxDate = new Date(now);
    maxDate.setDate(now.getDate() + 30);
    const maxLimitStr = toYMD(maxDate);

    // 去掉前导 0 的展示文案，例如: 11/4–12/4 · 2026
    const curMonth = now.getMonth() + 1;
    const curDay = now.getDate();
    const endMonth = maxDate.getMonth() + 1;
    const endDay = maxDate.getDate();

    const maxDisplayLabel = `${endMonth}/${endDay}`;
    const defaultRangeText = `${curMonth}/${curDay}–${endMonth}/${endDay} · ${now.getFullYear()}`;

    setDateBounds({
      todayStr,
      maxLimitStr,
      maxDisplayLabel,
      defaultRangeText,
    });
  }, []);

  const curStart = filters.customStartDate || dateBounds.todayStr;
  const curEnd = filters.customEndDate || dateBounds.maxLimitStr;

  const toggleArrayItem = <T extends string>(list: T[], item: T): T[] => {
    return list.includes(item) ? list.filter((i) => i !== item) : [...list, item];
  };

  return (
    // 独立悬浮白底卡片
    <div className="w-full bg-white rounded-2xl shadow-sm border border-slate-200/80 p-5 text-slate-700 text-sm select-none">
      <div className="flex flex-col gap-4">
        
        {/* 第一行：时间预设与搜索 */}
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3 flex-wrap">
            <div className="inline-flex rounded-xl bg-slate-100/90 p-1 text-xs font-medium text-slate-600 border border-slate-200/50">
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'month_and_next' })}
                className={`px-3.5 py-1.5 rounded-lg transition-all ${
                  filters.datePreset === 'month_and_next'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                未来30天
              </button>
              <button
                type="button"
                onClick={() => onChange({ ...filters, datePreset: 'this_weekend' })}
                className={`px-3.5 py-1.5 rounded-lg transition-all ${
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
                className={`px-3.5 py-1.5 rounded-lg transition-all ${
                  filters.datePreset === 'next_weekend'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                下周末
              </button>
              <button
                type="button"
                onClick={() =>
                  onChange({
                    ...filters,
                    datePreset: 'custom',
                    customStartDate: curStart,
                    customEndDate: curEnd,
                  })
                }
                className={`px-3.5 py-1.5 rounded-lg transition-all ${
                  filters.datePreset === 'custom'
                    ? 'bg-white text-slate-900 shadow-sm font-semibold'
                    : 'hover:text-slate-900'
                }`}
              >
                自选日期
              </button>
            </div>

            {filters.datePreset === 'custom' ? (
              <div className="inline-flex items-center gap-2 text-xs text-slate-600 bg-slate-50 border border-slate-200/80 px-2.5 py-1 rounded-xl">
                <input
                  type="date"
                  min={dateBounds.todayStr}
                  max={dateBounds.maxLimitStr}
                  value={curStart}
                  onChange={(e) => onChange({ ...filters, customStartDate: e.target.value })}
                  className="bg-white border border-slate-300 rounded-md px-2 py-1 text-xs text-slate-800 font-mono shadow-2xs focus:outline-none"
                />
                <span className="text-slate-400">至</span>
                <input
                  type="date"
                  min={curStart}
                  max={dateBounds.maxLimitStr}
                  value={curEnd}
                  onChange={(e) => onChange({ ...filters, customEndDate: e.target.value })}
                  className="bg-white border border-slate-300 rounded-md px-2 py-1 text-xs text-slate-800 font-mono shadow-2xs focus:outline-none"
                />
                {dateBounds.maxDisplayLabel && (
                  <span className="text-slate-400 font-mono text-[11px] ml-1">
                    可选至 {dateBounds.maxDisplayLabel}
                  </span>
                )}
              </div>
            ) : (
              <span className="text-xs text-slate-400 font-mono ml-1 hidden sm:inline">
                {dateBounds.defaultRangeText}
              </span>
            )}
          </div>

          {/* 搜索栏 */}
          <div className="relative min-w-[260px] max-w-sm flex-1 sm:flex-initial">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              placeholder="搜索活动、场馆、城市..."
              value={filters.searchQuery}
              onChange={(e) => onChange({ ...filters, searchQuery: e.target.value })}
              className="w-full bg-slate-100/80 hover:bg-slate-200/60 focus:bg-white text-xs text-slate-800 pl-10 pr-4 py-2 rounded-xl border border-transparent focus:border-slate-300 focus:outline-none focus:ring-2 focus:ring-slate-100 transition-all placeholder:text-slate-400"
            />
          </div>
        </div>

        {/* 第二行：复选条件 */}
        <div className="flex flex-wrap items-center gap-x-6 gap-y-2.5 text-xs text-slate-600 pt-1">
          <div className="flex items-center gap-2.5">
            <span className="text-slate-400 font-medium">地区</span>
            <div className="flex items-center gap-2.5">
              {REGION_OPTIONS.map((item) => {
                const checked = filters.regions.includes(item.key);
                return (
                  <label
                    key={item.key}
                    onClick={() =>
                      onChange({
                        ...filters,
                        regions: toggleArrayItem(filters.regions, item.key),
                      })
                    }
                    className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 transition-colors py-0.5"
                  >
                    <span
                      className={`w-4 h-4 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white shadow-xs'
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

          <div className="h-3.5 w-[1px] bg-slate-200 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <span className="text-slate-400 font-medium">年龄</span>
            <div className="flex items-center gap-2.5">
              {AGE_OPTIONS.map((item) => {
                const checked = filters.ageBuckets.includes(item.key);
                return (
                  <label
                    key={item.key}
                    onClick={() =>
                      onChange({
                        ...filters,
                        ageBuckets: toggleArrayItem(filters.ageBuckets, item.key),
                      })
                    }
                    className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 transition-colors py-0.5"
                  >
                    <span
                      className={`w-4 h-4 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white shadow-xs'
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

          <div className="h-3.5 w-[1px] bg-slate-200 hidden sm:block" />

          <div className="flex items-center gap-2.5">
            <span className="text-slate-400 font-medium">时段</span>
            <div className="flex items-center gap-2.5">
              {TIME_OPTIONS.map((item) => {
                const checked = filters.timeSlots.includes(item.key);
                return (
                  <label
                    key={item.key}
                    onClick={() =>
                      onChange({
                        ...filters,
                        timeSlots: toggleArrayItem(filters.timeSlots, item.key),
                      })
                    }
                    className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 transition-colors py-0.5"
                  >
                    <span
                      className={`w-4 h-4 rounded flex items-center justify-center border transition-colors ${
                        checked
                          ? 'bg-slate-900 border-slate-900 text-white shadow-xs'
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

          <div className="h-3.5 w-[1px] bg-slate-200 hidden md:block" />

          <div className="flex items-center gap-4">
            <label 
              onClick={() => onChange({ ...filters, isFreeOnly: !filters.isFreeOnly })}
              className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 transition-colors py-0.5"
            >
              <span
                className={`w-4 h-4 rounded flex items-center justify-center border transition-colors ${
                  filters.isFreeOnly
                    ? 'bg-slate-900 border-slate-900 text-white shadow-xs'
                    : 'border-slate-300 bg-white hover:border-slate-400'
                }`}
              >
                {filters.isFreeOnly && <Check className="w-2.5 h-2.5 stroke-[3]" />}
              </span>
              <Ticket className="w-3.5 h-3.5 text-slate-500" />
              <span>免费入场</span>
            </label>

            <label 
              onClick={() => onChange({ ...filters, isIndoorOnly: !filters.isIndoorOnly })}
              className="flex items-center gap-1.5 cursor-pointer hover:text-slate-900 transition-colors py-0.5"
            >
              <span
                className={`w-4 h-4 rounded flex items-center justify-center border transition-colors ${
                  filters.isIndoorOnly
                    ? 'bg-slate-900 border-slate-900 text-white shadow-xs'
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

        {/* 第三行：分类胶囊 */}
        <div className="flex items-center gap-2 overflow-x-auto pt-1 no-scrollbar">
          {CATEGORY_TABS.map((tab) => {
            const isActive = filters.category === tab.key;
            return (
              <button
                key={tab.key}
                type="button"
                onClick={() => onChange({ ...filters, category: tab.key })}
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-medium shrink-0 transition-all border ${
                  isActive
                    ? 'bg-slate-900 text-white border-slate-900 shadow-xs'
                    : 'bg-white text-slate-600 border-slate-200/80 hover:bg-slate-50 hover:text-slate-900 hover:border-slate-300'
                }`}
              >
                {tab.icon && (
                  <span className={isActive ? 'text-white' : 'text-slate-500'}>
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