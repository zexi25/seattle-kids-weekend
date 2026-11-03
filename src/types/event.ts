// src/types/event.ts

// 1. 基础枚举类型定义
export type RegionKey = 'seattle' | 'eastside' | 'north' | 'south';
export type AgeBucket = 'preschool' | 'elementary';
export type TimeSlot = 'morning' | 'afternoon';
export type EnvironmentType = 'indoor' | 'outdoor' | 'hybrid';
export type ParkingType = 'free_lot' | 'paid_garage' | 'street_parking' | 'transit_recommended';

export type CategoryKey = 
  | 'all'
  | 'nature_animals'    // 自然与动物
  | 'music_crafts'      // 音乐与手作
  | 'festivals_markets' // 节庆与市集
  | 'exploration_exp';  // 探索与体验

// 2. 地理位置信息
export interface EventLocation {
  venueName: string;
  address: string;
  city: string;
  neighborhood?: string;
  region: RegionKey;
  googleMapsUrl: string;
}

// 3. 排期与时间信息
export interface EventSchedule {
  startDate: string; // YYYY-MM-DD
  endDate: string;   // YYYY-MM-DD
  timeSlot?: TimeSlot;
  displayTime: string; // 例如: "11/7 周六 · 10:30–11:15"
  timezone?: string;
}

// 4. 亲子特定核心属性（严格类型声明，避免 Implicit Any）
export interface FamilyAttributes {
  ageBuckets: AgeBucket[];
  environment: EnvironmentType;
  isFree: boolean;
  priceLabel: string; // 例如: "免费入场" 或 "门票 $15"
  requiresRsvp?: boolean;
  strollerFriendly?: boolean;
  hasChangingTable?: boolean;
  parking?: ParkingType;
}

// 5. 来源元数据
export interface EventSource {
  originalUrl: string;
  sourceName?: string;
  crawledAt?: string;
}

// 6. 活动的核心属性集合
export interface EventProperties {
  title: string;
  summary: string;
  organizer: string;
  category: Exclude<CategoryKey, 'all'>;
  tags?: string[];
  location: EventLocation;
  schedule: EventSchedule;
  familyAttributes: FamilyAttributes;
  source: EventSource;
}

// 7. 标准 GeoJSON 规范结构
export interface WeekendEventFeature {
  type: 'Feature';
  id: string;
  geometry: {
    type: 'Point';
    coordinates: [number, number]; // [经度 lng, 纬度 lat]
  };
  properties: EventProperties;
}

export interface WeekendEventGeoJSON {
  type: 'FeatureCollection';
  metadata?: {
    generatedAt: string;
    region: string;
    totalCount: number;
  };
  features: WeekendEventFeature[];
}