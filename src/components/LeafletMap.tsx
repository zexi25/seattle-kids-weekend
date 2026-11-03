// src/components/LeafletMap.tsx
'use client';

import React, { useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import { ExternalLink, X } from 'lucide-react';
import { WeekendEventFeature } from '@/types/event';

interface LeafletMapProps {
  events: WeekendEventFeature[];
  selectedId: string | null;
  onSelectEvent: (id: string | null) => void;
}

// 辅助组件：处理选中点位时的地图飞行定位 (FlyTo)
function FlyToSelected({ center }: { center?: [number, number] }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, 13, { duration: 0.8 });
    }
  }, [center, map]);
  return null;
}

export default function LeafletMap({
  events,
  selectedId,
  onSelectEvent,
}: LeafletMapProps) {
  // 西雅图市中心默认中心点
  const defaultCenter: [number, number] = [47.6062, -122.3321];

  const selectedEvent = events.find((e) => e.id === selectedId);
  const activeCoord: [number, number] | undefined = selectedEvent
    ? [selectedEvent.geometry.coordinates[1], selectedEvent.geometry.coordinates[0]]
    : undefined;

  return (
    <div className="relative w-full h-full">
      {/* 悬浮地点统计徽标 */}
      <div className="absolute top-4 left-4 z-[400] bg-white/95 backdrop-blur px-3 py-1.5 rounded-md shadow-sm border border-slate-200 text-xs font-medium text-slate-700 flex items-center gap-2 select-none">
        <span className="h-2 w-2 rounded-full bg-slate-900" />
        <span>{events.length} 个地点</span>
      </div>

      <MapContainer
        center={defaultCenter}
        zoom={10}
        scrollWheelZoom={true}
        className="h-full w-full z-0"
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        <FlyToSelected center={activeCoord} />

        {/* 渲染所有点位 */}
        {events.map((evt) => {
          const isSelected = evt.id === selectedId;
          const [lng, lat] = evt.geometry.coordinates;

          return (
            <CircleMarker
              key={evt.id}
              center={[lat, lng]}
              radius={isSelected ? 9 : 5.5}
              pathOptions={{
                color: isSelected ? '#0f172a' : '#ffffff',
                weight: isSelected ? 3.5 : 1.5,
                fillColor: isSelected ? '#ffffff' : '#334155',
                fillOpacity: isSelected ? 1 : 0.9,
              }}
              eventHandlers={{
                click: () => onSelectEvent(evt.id),
              }}
            />
          );
        })}
      </MapContainer>

      {/* 地图底部悬浮卡片（选中时出现） */}
      {selectedEvent && (
        <div className="absolute bottom-6 left-1/2 -translate-x-1/2 z-[400] w-[92%] max-w-md bg-white/95 backdrop-blur-md rounded-xl p-4 shadow-xl border border-slate-200 transition-all select-none">
          <div className="flex justify-between items-start gap-2">
            <div>
              <div className="text-[11px] text-slate-500 font-medium">
                {selectedEvent.properties.location.city} ·{' '}
                {selectedEvent.properties.familyAttributes.priceLabel}
              </div>
              <h3 className="text-sm font-bold text-slate-900 mt-0.5 line-clamp-1">
                {selectedEvent.properties.title}
              </h3>
              <p className="text-xs text-slate-500 mt-1 truncate">
                📍 {selectedEvent.properties.location.venueName}
              </p>
              <p className="text-[11px] text-slate-400 mt-0.5 font-mono">
                {selectedEvent.properties.schedule.displayTime}
              </p>
            </div>
            <button
              type="button"
              onClick={() => onSelectEvent(null)}
              className="text-slate-400 hover:text-slate-600 p-1 rounded-md transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="mt-3 pt-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-[11px] text-slate-400">
              适龄: {selectedEvent.properties.familyAttributes.ageBuckets.join('/')}
            </span>
            <a
              href={selectedEvent.properties.source.originalUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-700 font-medium inline-flex items-center gap-1"
            >
              <span>查看原文</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      )}
    </div>
  );
}