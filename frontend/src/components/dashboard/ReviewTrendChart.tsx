"use client";

import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const data = [
  { name: "Jan", total: 104 },
  { name: "Feb", total: 120 },
  { name: "Mar", total: 145 },
  { name: "Apr", total: 198 },
  { name: "May", total: 240 },
  { name: "Jun", total: 310 },
  { name: "Jul", total: 420 },
];

export function ReviewTrendChart() {
  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart data={data}>
        <XAxis
          dataKey="name"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
          tickFormatter={(value) => `${value}`}
        />
        <Tooltip
          contentStyle={{ backgroundColor: "var(--background)", borderColor: "var(--border)", borderRadius: "var(--radius)" }}
          itemStyle={{ color: "var(--foreground)" }}
        />
        <Line
          type="monotone"
          dataKey="total"
          stroke="var(--primary)"
          strokeWidth={2}
          activeDot={{ r: 8 }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
