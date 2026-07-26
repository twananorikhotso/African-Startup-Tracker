package com.africa.backend.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "startups")
public class Startup {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String company;

    private String country;

    private String sector;

    private Integer funding;

    public Startup() {
    }

    public Startup(String company, String country, String sector, Integer funding) {
        this.company = company;
        this.country = country;
        this.sector = sector;
        this.funding = funding;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getCompany() {
        return company;
    }

    public void setCompany(String company) {
        this.company = company;
    }

    public String getCountry() {
        return country;
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getSector() {
        return sector;
    }

    public void setSector(String sector) {
        this.sector = sector;
    }

    public Integer getFunding() {
        return funding;
    }

    public void setFunding(Integer funding) {
        this.funding = funding;
    }
}
