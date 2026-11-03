// src/components/EventList.tsx
'use client';

import React from 'react';
import { 
  ArrowLeft, 
  MapPin, 
  Calendar, 
  ExternalLink, 
  Navigation, 
  Sparkles, 
  Leaf, 
  Music, 
  Compass 
} from 'lucide-react';
import { WeekendEventFeature } from '@/types/event';

interface EventListProps {
  events: WeekendEventFeature[];
  selectedId: string | null;
  onSelectEvent: (id: string | null) => void;
  onClearFilters: () => void;
}

// 对应类型小图标映射
const CATEGORY_ICON_MAP: Record<string, React.ReactNode> = {
  nature_animals: <Leaf className="w-3.5 h-3.5 text-emerald-600" />,
  music_crafts: <Music className="w-3.5 h-3.5 text-indigo-600" />,
  festivals_markets: <Sparkles className="w-3.5 h-3.5 text-amber-500" />,
  exploration_exp: <Compass className="w-3.5 h-3.5 text-blue-600" />,
};

export default function EventList({
  events,
  selectedId,
  onSelectEvent,
  onClearFilters,
}: EventListProps) {
  const selectedEvent = events.find((e) => e.id === selectedId);

  // 1. 详情视图（用户点击卡片后展示）
  if (selectedEvent) {
    const p = selectedEvent.properties;
    return (
      <div className="flex flex-col h-full bg-white overflow-y-auto">
        {/* 顶部返回导航 */}
        <div className="sticky top-0 z-10 bg-white/95 backdrop-blur px-6 py-3 border-b border-slate-100 flex items-center justify-between">
          <button
            type="button"
            onClick={() => onSelectEvent(null)}
            className="inline-flex items-center gap-1.5 text-xs font-medium text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>返回活动列表</span>
          </button>
          <span className="text-xs text-slate-400 font-mono">
            {p.location.city} · {p.familyAttributes.priceLabel}
          </span>
        </div>

        {/* 详情内容 */}
        <div className="p-6 space-y-5 flex-1">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-[11px] font-medium">
                {p.familyAttributes.priceLabel}
              </span>
              <span className="text-xs text-slate-400">{p.organizer}</span>
            </div>
            <h1 className="text-lg font-bold text-slate-900 leading-snug">
              {p.title}
            </h1>
          </div>

          {/* 场地与定位 */}
          <div className="flex items-start gap-2 text-xs text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-100">
            <MapPin className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-semibold text-slate-800">{p.location.venueName}</div>
              <div className="text-slate-500 mt-0.5">{p.location.address}</div>
            </div>
          </div>

          {/* 活动摘要 */}
          <div className="text-xs text-slate-600 leading-relaxed space-y-2 border-b border-slate-100 pb-5">
            <p>{p.summary}</p>
          </div>

          {/* 关键亲子属性参数 */}
          <div className="grid grid-cols-2 gap-3 text-xs">
            <div className="border border-slate-100 p-2.5 rounded-md">
              <div className="text-slate-400 text-[11px]">适龄参考</div>
              <div className="font-medium text-slate-800 mt-0.5">
                {p.familyAttributes.ageBuckets
                  .map((b: string) => (b === 'preschool' ? '学龄前 (0–5岁)' : '小学 (6–12岁)'))
                  .join(' / ')}
              </div>
            </div>
            <div className="border border-slate-100 p-2.5 rounded-md">
              <div className="text-slate-400 text-[11px]">环境与停车</div>
              <div className="font-medium text-slate-800 mt-0.5">
                {p.familyAttributes.environment === 'indoor' ? '室内' : '户外'} ·{' '}
                {p.familyAttributes.parking === 'free_lot'
                  ? '免费车位'
                  : p.familyAttributes.parking === 'paid_garage'
                  ? '收费车库'
                  : '街趴'}
              </div>
            </div>
          </div>

          {/* 时间日程 */}
          <div className="text-xs space-y-1.5 border-t border-slate-100 pt-4">
            <div className="font-semibold text-slate-700">排期时间</div>
            <div className="flex items-center gap-2 text-slate-600 font-mono">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              <span>{p.schedule.displayTime}</span>
            </div>
          </div>

          {/* 操作按钮组 */}
          <div className="flex items-center gap-3 pt-3">
            <a
              href={p.source.originalUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 inline-flex items-center justify-center gap-1.5 bg-slate-900 hover:bg-slate-800 text-white text-xs font-medium py-2.5 px-4 rounded-lg transition-colors"
            >
              <span>原文 / 预约</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
            <a
              href={p.location.googleMapsUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-1.5 border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-medium py-2.5 px-4 rounded-lg transition-colors"
            >
              <Navigation className="w-3.5 h-3.5" />
              <span>打开导航</span>
            </a>
          </div>
        </div>
      </div>
    );
  }

  // 2. 列表视图（默认滚动长列表）
  return (
    <div className="flex flex-col h-full bg-white">
      {/* 计数统计与清除筛选 */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-slate-100 bg-slate-50/60 shrink-0">
        <span className="text-xs font-semibold text-slate-700">
          {events.length} 个活动
        </span>
        <button
          type="button"
          onClick={onClearFilters}
          className="text-xs text-slate-400 hover:text-slate-600 transition-colors"
        >
          ✕ 清除筛选
        </button>
      </div>

      {/* 活动流 */}
      <div className="flex-1 overflow-y-auto divide-y divide-slate-100 px-6">
        {events.length === 0 ? (
          <div className="py-20 text-center text-xs text-slate-400">
            暂无符合条件的活动，请尝试放宽筛选条件
          </div>
        ) : (
          events.map((evt) => {
            const p = evt.properties;
            return (
              <article
                key={evt.id}
                onClick={() => onSelectEvent(evt.id)}
                className="py-4 cursor-pointer hover:bg-slate-50/70 transition-colors group select-none"
              >
                {/* 顶部标签 */}
                <div className="flex items-center justify-between text-xs mb-1">
                  <div className="flex items-center gap-2">
                    <span className="text-slate-500 font-medium">{p.location.city}</span>
                    <span className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[11px]">
                      {p.familyAttributes.priceLabel}
                    </span>
                  </div>
                  <span>{CATEGORY_ICON_MAP[p.category] || null}</span>
                </div>

                {/* 标题 */}
                <h2 className="text-sm font-bold text-slate-900 group-hover:text-blue-600 transition-colors mb-1 line-clamp-1">
                  {p.title}
                </h2>

                {/* 地点 */}
                <div className="flex items-center gap-1 text-[11px] text-slate-500 mb-2">
                  <MapPin className="w-3 h-3 text-slate-400 shrink-0" />
                  <span className="truncate">{p.location.venueName}</span>
                </div>

                {/* 摘要 */}
                <p className="text-xs text-slate-500 leading-relaxed line-clamp-2 mb-3">
                  {p.summary}
                </p>

                {/* 排期 */}
                <div className="text-[11px] text-slate-400 font-mono flex items-center gap-1.5">
                  <Calendar className="w-3 h-3 text-slate-400" />
                  <span>{p.schedule.displayTime}</span>
                </div>
              </article>
            );
          })
        )}
      </div>

      {/* 底部免责声明 */}
      <footer className="border-t border-slate-100 px-6 py-2 text-[11px] text-slate-400 bg-slate-50/50 shrink-0">
        时间均为西雅图当地时间，费用及预约以活动原文为准。
      </footer>
    </div>
  );
}