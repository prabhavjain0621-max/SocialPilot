import type { ReactNode } from 'react';

type Props = {
  children?: ReactNode;
  className?: string;
  hover?: boolean;
  onClick?: () => void;
};

export default function Card({ children, className = '', hover = false, onClick }: Props) {
  return (
    <div
      onClick={onClick}
      className={`bg-white dark:bg-ink-900 border border-ink-100 dark:border-ink-800 rounded-2xl shadow-soft dark:shadow-none transition-colors duration-200 ${
        hover ? 'transition-all duration-300 hover:shadow-lift dark:hover:shadow-glow hover:border-ink-200 dark:hover:border-ink-700 hover:-translate-y-0.5' : ''
      } ${onClick ? 'cursor-pointer' : ''} ${className}`}
    >
      {children}
    </div>
  );
}
