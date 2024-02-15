package com.example.mdp_group31.main;

import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;
import androidx.viewpager2.adapter.FragmentStateAdapter;

import java.util.ArrayList;


public class SectionsPagerAdapter extends FragmentStateAdapter {

    private final ArrayList<Fragment> fragmentArrayList = new ArrayList<>();
    private final ArrayList<String> fragmentTitle = new ArrayList<>();


    public SectionsPagerAdapter(FragmentActivity fragmentActivity) {
        super(fragmentActivity);
    }

    @Override
    public Fragment createFragment(int position) {
        return fragmentArrayList.get(position);
    }

    @Override
    public int getItemCount() {
        // Return the total number of fragments
        return fragmentArrayList.size();
    }

    public String getTabTitle(int position) {
        return fragmentTitle.get(position);
    }

    public Fragment getItem(int position) {
        return fragmentArrayList.get(position);
    }

    @Nullable
    public CharSequence getPageTitle(int position) {
        return fragmentTitle.get(position);
    }

    public int getCount() {
        return fragmentArrayList.size();
    }

    public void addFragment(Fragment fm, String title){
        fragmentArrayList.add(fm);
        fragmentTitle.add(title);
    }
}